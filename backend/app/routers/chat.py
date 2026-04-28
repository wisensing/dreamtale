import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.kid import Kid
from app.models.chat import ChatSession, ChatMessage, MessageRole
from app.models.story import Story
from app.schemas.chat import (
    ChatSessionCreate, ChatMessageSend, ChatSessionOut, ChatMessageOut, ChatSessionDetail,
)
from app.auth.supabase import get_current_user
from app.services.story_engine import generate_story, modify_story
from app.services.credit_service import can_generate_story, deduct_credit, InsufficientCreditsError

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/sessions", response_model=ChatSessionOut, status_code=status.HTTP_201_CREATED)
async def create_session(
    request: ChatSessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    kid_result = await db.execute(
        select(Kid).where(Kid.id == uuid.UUID(request.kid_id), Kid.user_id == current_user.id)
    )
    kid = kid_result.scalar_one_or_none()
    if not kid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kid not found")

    session = ChatSession(kid_id=kid.id, title=request.title)
    db.add(session)
    await db.flush()
    return ChatSessionOut.model_validate(session)


@router.get("/sessions", response_model=list[ChatSessionOut])
async def list_sessions(
    kid_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    kid_result = await db.execute(
        select(Kid).where(Kid.id == uuid.UUID(kid_id), Kid.user_id == current_user.id)
    )
    kid = kid_result.scalar_one_or_none()
    if not kid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kid not found")

    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.kid_id == kid.id)
        .order_by(ChatSession.updated_at.desc())
    )
    return [ChatSessionOut.model_validate(s) for s in result.scalars().all()]


@router.get("/sessions/{session_id}", response_model=ChatSessionDetail)
async def get_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ChatSession).where(ChatSession.id == uuid.UUID(session_id)))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    kid_result = await db.execute(select(Kid).where(Kid.id == session.kid_id))
    kid = kid_result.scalar_one_or_none()
    if not kid or kid.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    messages_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.chat_session_id == session.id)
        .order_by(ChatMessage.created_at)
    )
    messages = messages_result.scalars().all()

    return ChatSessionDetail(
        id=str(session.id),
        kid_id=str(session.kid_id),
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        messages=[ChatMessageOut.model_validate(m) for m in messages],
    )


@router.post("/sessions/{session_id}/messages", response_model=ChatMessageOut)
async def send_message(
    session_id: str,
    request: ChatMessageSend,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(ChatSession).where(ChatSession.id == uuid.UUID(session_id)))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    kid_result = await db.execute(select(Kid).where(Kid.id == session.kid_id))
    kid = kid_result.scalar_one_or_none()
    if not kid or kid.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    user_message = ChatMessage(
        chat_session_id=session.id,
        role=MessageRole.user,
        content=request.content,
    )
    db.add(user_message)
    await db.flush()

    content_lower = request.content.lower()
    is_modification = any(
        word in content_lower
        for word in ["change", "modify", "make it", "different", "instead", "but", "again"]
    )

    story_id = None
    if is_modification:
        last_story_result = await db.execute(
            select(ChatMessage)
            .where(
                ChatMessage.chat_session_id == session.id,
                ChatMessage.story_id.isnot(None),
            )
            .order_by(ChatMessage.created_at.desc())
            .limit(1)
        )
        last_story_msg = last_story_result.scalar_one_or_none()
        if last_story_msg:
            story_result = await db.execute(
                select(Story).where(Story.id == last_story_msg.story_id)
            )
            story = story_result.scalar_one_or_none()
            if story:
                try:
                    story = await modify_story(db, story, request.content, kid)
                    story_id = story.id
                    response_text = f"Here's the modified version of your story! {story.theme}"
                except ValueError as e:
                    response_text = f"I couldn't modify the story: {str(e)}"
        else:
            is_modification = False

    if not is_modification:
        if not can_generate_story(current_user):
            assistant_message = ChatMessage(
                chat_session_id=session.id,
                role=MessageRole.assistant,
                content="I'd love to tell you a story, but you're out of credits! You can get more in the Credits section.",
            )
            db.add(assistant_message)
            await db.flush()
            return ChatMessageOut.model_validate(assistant_message)

        try:
            story = await generate_story(
                db=db, kid=kid, keywords=request.content, chat_session_id=session.id,
            )
            await deduct_credit(db, current_user, description=f"Story: {story.theme}")
            story_id = story.id
            response_text = story.text
            session.title = request.content[:50] if len(request.content) > 50 else request.content
            db.add(session)
        except (ValueError, InsufficientCreditsError) as e:
            assistant_message = ChatMessage(
                chat_session_id=session.id,
                role=MessageRole.assistant,
                content=f"I had trouble creating a story: {str(e)}",
            )
            db.add(assistant_message)
            await db.flush()
            return ChatMessageOut.model_validate(assistant_message)

    assistant_message = ChatMessage(
        chat_session_id=session.id,
        role=MessageRole.assistant,
        content=response_text,
        story_id=story_id,
    )
    db.add(assistant_message)
    await db.flush()
    return ChatMessageOut.model_validate(assistant_message)
