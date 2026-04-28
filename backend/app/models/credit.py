import uuid
import enum

from sqlalchemy import String, Integer, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.database import Base


class TransactionType(str, enum.Enum):
    purchase = "purchase"
    usage = "usage"
    bonus = "bonus"
    refund = "refund"


class CreditTransaction(Base):
    __tablename__ = "credit_transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    amount: Mapped[int] = mapped_column(Integer)
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    description: Mapped[str] = mapped_column(String)
    stripe_payment_id: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", backref="credit_transactions")
