import uuid

from sqlalchemy import Date, Time, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone, date

from app.database import Base


class BedtimeSession(Base):
    __tablename__ = "bedtime_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kid_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("kids.id"), index=True)
    date: Mapped[date] = mapped_column(Date)
    bedtime_actual: Mapped[str] = mapped_column(String)
    story_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stories.id"), nullable=True
    )
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    kid = relationship("Kid", backref="bedtime_sessions")
    story = relationship("Story")
