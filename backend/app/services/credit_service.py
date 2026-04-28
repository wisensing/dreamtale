from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, SubscriptionTier
from app.models.credit import CreditTransaction, TransactionType


class InsufficientCreditsError(Exception):
    pass


FREE_STORIES = 3
CREDIT_PACKS = {
    "10": {"credits": 10, "price_cents": 499},
    "25": {"credits": 25, "price_cents": 999},
    "50": {"credits": 50, "price_cents": 1499},
    "100": {"credits": 100, "price_cents": 2499},
}


def can_generate_story(user: User) -> bool:
    if user.subscription_tier in (SubscriptionTier.premium, SubscriptionTier.family):
        return True
    return user.credit_balance > 0


async def deduct_credit(db: AsyncSession, user: User, description: str = "Story generation") -> None:
    if user.subscription_tier in (SubscriptionTier.premium, SubscriptionTier.family):
        return

    if user.credit_balance <= 0:
        raise InsufficientCreditsError("No credits remaining. Please purchase more credits.")

    user.credit_balance -= 1
    transaction = CreditTransaction(
        user_id=user.id,
        amount=-1,
        transaction_type=TransactionType.usage,
        description=description,
    )
    db.add(transaction)


async def add_credits(
    db: AsyncSession,
    user: User,
    amount: int,
    transaction_type: TransactionType,
    description: str,
    stripe_payment_id: str | None = None,
) -> None:
    user.credit_balance += amount
    transaction = CreditTransaction(
        user_id=user.id,
        amount=amount,
        transaction_type=transaction_type,
        description=description,
        stripe_payment_id=stripe_payment_id,
    )
    db.add(transaction)
