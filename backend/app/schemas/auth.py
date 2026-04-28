from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.user import SubscriptionTier


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    coppa_consent: bool = False


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"


class UserOut(BaseModel):
    id: str
    email: str
    subscription_tier: SubscriptionTier
    credit_balance: int
    coppa_consent: bool
    content_strictness: int
    created_at: datetime

    model_config = {"from_attributes": True}
