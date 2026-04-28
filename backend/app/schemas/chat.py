from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.chat import MessageRole


class ChatSessionCreate(BaseModel):
    kid_id: str
    title: str = "New Chat"


class ChatMessageSend(BaseModel):
    content: str


class ChatSessionOut(BaseModel):
    id: str
    kid_id: str
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ChatMessageOut(BaseModel):
    id: str
    chat_session_id: str
    role: MessageRole
    content: str
    story_id: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatSessionDetail(BaseModel):
    id: str
    kid_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[ChatMessageOut]

    model_config = {"from_attributes": True}
