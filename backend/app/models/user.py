import uuid
import enum

from sqlalchemy import String, Boolean, Integer, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from app.database import Base


class SubscriptionTier(str, enum.Enum):
    free = "free"
    premium = "premium"
    family = "family"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supabase_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    subscription_tier: Mapped[SubscriptionTier] = mapped_column(
        Enum(SubscriptionTier), default=SubscriptionTier.free
    )
    credit_balance: Mapped[int] = mapped_column(Integer, default=3)
    coppa_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    coppa_consent_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    content_strictness: Mapped[int] = mapped_column(Integer, default=3)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )
