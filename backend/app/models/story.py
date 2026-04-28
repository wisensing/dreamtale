import uuid

from sqlalchemy import String, Text, Boolean, Integer, Float, ForeignKey, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.database import Base


class Story(Base):
    __tablename__ = "stories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kid_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("kids.id"), index=True)
    chat_session_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chat_sessions.id"), nullable=True
    )
    text: Mapped[str] = mapped_column(Text)
    audio_url: Mapped[str | None] = mapped_column(String, nullable=True)
    theme: Mapped[str] = mapped_column(String, default="")
    educational_topic: Mapped[str] = mapped_column(String, default="")
    story_style: Mapped[str] = mapped_column(String, default="")
    language: Mapped[str] = mapped_column(String, default="en")
    keywords_used: Mapped[list] = mapped_column(JSON, default=list)
    is_saved: Mapped[bool] = mapped_column(Boolean, default=False)
    play_count: Mapped[int] = mapped_column(Integer, default=0)
    safety_score: Mapped[float] = mapped_column(Float, default=1.0)
    parent_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    kid = relationship("Kid", backref="stories")
    versions = relationship("StoryVersion", backref="story", order_by="StoryVersion.version_number")
    translations = relationship("StoryTranslation", backref="story")


class StoryVersion(Base):
    __tablename__ = "story_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    story_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stories.id"), index=True)
    text: Mapped[str] = mapped_column(Text)
    audio_url: Mapped[str | None] = mapped_column(String, nullable=True)
    version_number: Mapped[int] = mapped_column(Integer)
    modification_prompt: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class StoryTranslation(Base):
    __tablename__ = "story_translations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    story_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stories.id"), index=True)
    language: Mapped[str] = mapped_column(String)
    translated_text: Mapped[str] = mapped_column(Text)
    audio_url: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class SharedStory(Base):
    __tablename__ = "shared_stories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    story_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stories.id"), index=True)
    share_token: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    story = relationship("Story", backref="shares")
