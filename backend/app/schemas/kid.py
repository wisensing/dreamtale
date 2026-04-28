from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class KidCreate(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=2, le=10)
    interests: list[str] = Field(default_factory=list)
    fears: list[str] = Field(default_factory=list)
    bedtime_goal: Optional[str] = None
    primary_language: str = "en"
    learning_languages: list[str] = Field(default_factory=list)
    companion_name: Optional[str] = None


class KidUpdate(BaseModel):
    nickname: Optional[str] = None
    age: Optional[int] = Field(None, ge=2, le=10)
    interests: Optional[list[str]] = None
    fears: Optional[list[str]] = None
    bedtime_goal: Optional[str] = None
    primary_language: Optional[str] = None
    learning_languages: Optional[list[str]] = None
    companion_name: Optional[str] = None


class KidOut(BaseModel):
    id: str
    nickname: str
    age: int
    interests: list[str]
    fears: list[str]
    bedtime_goal: Optional[str]
    primary_language: str
    learning_languages: list[str]
    companion_name: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
