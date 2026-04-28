from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.credit import CreditTransaction
from app.schemas.credit import CreditBalance, CheckoutRequest, CheckoutResponse, CreditTransactionOut
from app.auth.supabase import get_current_user
from app.services.credit_service import add_credits, CREDIT_PACKS
from app.models.credit import TransactionType

router = APIRouter(prefix="/credits", tags=["credits"])


@router.get("/balance", response_model=CreditBalance)
async def get_balance(
    current_user: User = Depends(get_current_user),
):
    return CreditBalance(
        balance=current_user.credit_balance,
        subscription_tier=current_user.subscription_tier.value,
    )


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(
    request: CheckoutRequest,
    current_user: User = Depends(get_current_user),
):
    if request.pack not in CREDIT_PACKS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credit pack")

    try:
        from app.services.stripe_service import create_checkout_session
        result = create_checkout_session(
            user_id=str(current_user.id),
            pack=request.pack,
            success_url="dreamtale://credits/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="dreamtale://credits/cancel",
        )
        return CheckoutResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    from app.services.stripe_service import verify_webhook_signature
    from app.models.user import User

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        event = verify_webhook_signature(payload, sig_header)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session_data = event["data"]["object"]
        user_id = session_data["metadata"]["user_id"]
        pack = session_data["metadata"]["pack"]

        pack_info = CREDIT_PACKS.get(pack)
        if not pack_info:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid pack")

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            await add_credits(
                db=db,
                user=user,
                amount=pack_info["credits"],
                transaction_type=TransactionType.purchase,
                description=f"Purchased {pack_info['credits']} credits",
                stripe_payment_id=session_data.get("payment_intent"),
            )

    return {"status": "ok"}


@router.get("/transactions", response_model=list[CreditTransactionOut])
async def list_transactions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(CreditTransaction)
        .where(CreditTransaction.user_id == current_user.id)
        .order_by(CreditTransaction.created_at.desc())
        .limit(50)
    )
    return [CreditTransactionOut.model_validate(t) for t in result.scalars().all()]
