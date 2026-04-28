import uuid

from sqlalchemy import String, Integer, Time, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.database import Base


class Kid(Base):
    __tablename__ = "kids"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    nickname: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    interests: Mapped[list] = mapped_column(JSON, default=list)
    fears: Mapped[list] = mapped_column(JSON, default=list)
    bedtime_goal: Mapped[str | None] = mapped_column(String, nullable=True)
    primary_language: Mapped[str] = mapped_column(String, default="en")
    learning_languages: Mapped[list] = mapped_column(JSON, default=list)
    companion_name: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", backref="kids")
