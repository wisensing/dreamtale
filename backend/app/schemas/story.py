from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class StoryGenerate(BaseModel):
    kid_id: str
    keywords: Optional[str] = None
    language: str = "en"
    story_style: str = ""


class StoryModify(BaseModel):
    modification: str
    language: Optional[str] = None


class StoryTranslate(BaseModel):
    target_language: str


class StorySave(BaseModel):
    is_saved: bool


class StoryShare(BaseModel):
    is_public: bool = True


class StoryOut(BaseModel):
    id: str
    kid_id: str
    text: str
    audio_url: Optional[str]
    theme: str
    educational_topic: str
    story_style: str
    language: str
    keywords_used: list[str]
    is_saved: bool
    play_count: int
    safety_score: float
    parent_rating: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}


class SharedStoryOut(BaseModel):
    story_text: str
    story_audio_url: Optional[str]
    story_theme: str
    story_language: str
    kid_nickname: str
    share_token: str

    model_config = {"from_attributes": True}


class StoryVersionOut(BaseModel):
    id: str
    version_number: int
    text: str
    modification_prompt: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class StoryTranslationOut(BaseModel):
    id: str
    language: str
    translated_text: str
    audio_url: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
