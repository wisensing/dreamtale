from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.credit import TransactionType


class CreditBalance(BaseModel):
    balance: int
    subscription_tier: str


class CheckoutRequest(BaseModel):
    pack: str  # "10", "25", "50", "100"


class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str


class CreditTransactionOut(BaseModel):
    id: str
    amount: int
    transaction_type: TransactionType
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}
