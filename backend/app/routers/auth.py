from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone

from app.database import get_db
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest, AuthResponse, UserOut
from app.auth.supabase import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest, db: AsyncSession = Depends(get_db)):
    from app.config import get_settings
    from supabase import create_client

    settings = get_settings()
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    try:
        auth_response = supabase.auth.sign_up({"email": request.email, "password": request.password})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    supabase_id = auth_response.user.id
    access_token = auth_response.session.access_token

    existing = await db.execute(select(User).where(User.supabase_id == supabase_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    user = User(
        supabase_id=supabase_id,
        email=request.email,
        coppa_consent=request.coppa_consent,
        coppa_consent_date=datetime.now(timezone.utc) if request.coppa_consent else None,
    )
    db.add(user)
    await db.flush()

    return AuthResponse(
        access_token=access_token,
        user=UserOut.model_validate(user),
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    from app.config import get_settings
    from supabase import create_client

    settings = get_settings()
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    try:
        auth_response = supabase.auth.sign_in_with_password({"email": request.email, "password": request.password})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    supabase_id = auth_response.user.id
    access_token = auth_response.session.access_token

    result = await db.execute(select(User).where(User.supabase_id == supabase_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return AuthResponse(
        access_token=access_token,
        user=UserOut.model_validate(user),
    )


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)
