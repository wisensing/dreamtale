import uuid
import secrets

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.kid import Kid
from app.models.story import Story, StoryVersion, StoryTranslation, SharedStory
from app.schemas.story import (
    StoryGenerate, StoryModify, StoryTranslate, StorySave, StoryShare,
    StoryOut, SharedStoryOut, StoryVersionOut, StoryTranslationOut,
)
from app.auth.supabase import get_current_user, get_optional_user
from app.services.story_engine import generate_story, modify_story, translate_story
from app.services.credit_service import can_generate_story, deduct_credit, InsufficientCreditsError

router = APIRouter(prefix="/stories", tags=["stories"])


@router.post("/generate", response_model=StoryOut)
async def generate(
    request: StoryGenerate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not can_generate_story(current_user):
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="No credits remaining. Please purchase more credits.",
        )

    result = await db.execute(
        select(Kid).where(Kid.id == uuid.UUID(request.kid_id), Kid.user_id == current_user.id)
    )
    kid = result.scalar_one_or_none()
    if not kid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kid not found")

    try:
        story = await generate_story(
            db=db,
            kid=kid,
            keywords=request.keywords,
            language=request.language,
            story_style=request.story_style,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    try:
        await deduct_credit(db, current_user, description=f"Story: {story.theme}")
    except InsufficientCreditsError as e:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=str(e))

    return StoryOut.model_validate(story)


@router.post("/{story_id}/modify", response_model=StoryOut)
async def modify(
    story_id: str,
    request: StoryModify,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Story).where(Story.id == uuid.UUID(story_id)))
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    kid_result = await db.execute(select(Kid).where(Kid.id == story.kid_id))
    kid = kid_result.scalar_one_or_none()
    if not kid or kid.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    try:
        story = await modify_story(db, story, request.modification, kid, request.language)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return StoryOut.model_validate(story)


@router.get("", response_model=list[StoryOut])
async def list_stories(
    kid_id: str | None = Query(None),
    is_saved: bool | None = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Story).join(Kid).where(Kid.user_id == current_user.id)
    if kid_id:
        query = query.where(Story.kid_id == uuid.UUID(kid_id))
    if is_saved is not None:
        query = query.where(Story.is_saved == is_saved)
    query = query.order_by(Story.created_at.desc()).limit(limit).offset(offset)

    result = await db.execute(query)
    return [StoryOut.model_validate(s) for s in result.scalars().all()]


@router.get("/{story_id}", response_model=StoryOut)
async def get_story(
    story_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Story).where(Story.id == uuid.UUID(story_id)))
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    kid_result = await db.execute(select(Kid).where(Kid.id == story.kid_id))
    kid = kid_result.scalar_one_or_none()
    if not kid or kid.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    return StoryOut.model_validate(story)


@router.post("/{story_id}/save", response_model=StoryOut)
async def save_story(
    story_id: str,
    request: StorySave,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Story).where(Story.id == uuid.UUID(story_id)))
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    kid_result = await db.execute(select(Kid).where(Kid.id == story.kid_id))
    kid = kid_result.scalar_one_or_none()
    if not kid or kid.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    story.is_saved = request.is_saved
    db.add(story)
    await db.flush()
    return StoryOut.model_validate(story)


@router.post("/{story_id}/share", response_model=SharedStoryOut)
async def share_story(
    story_id: str,
    request: StoryShare,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Story).where(Story.id == uuid.UUID(story_id)))
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    kid_result = await db.execute(select(Kid).where(Kid.id == story.kid_id))
    kid = kid_result.scalar_one_or_none()
    if not kid or kid.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    existing = await db.execute(
        select(SharedStory).where(SharedStory.story_id == story.id)
    )
    shared = existing.scalar_one_or_none()
    if shared:
        shared.is_public = request.is_public
    else:
        share_token = secrets.token_urlsafe(16)
        shared = SharedStory(story_id=story.id, share_token=share_token, is_public=request.is_public)
        db.add(shared)

    await db.flush()

    return SharedStoryOut(
        story_text=story.text,
        story_audio_url=story.audio_url,
        story_theme=story.theme,
        story_language=story.language,
        kid_nickname=kid.nickname,
        share_token=shared.share_token,
    )


@router.get("/shared/{token}", response_model=SharedStoryOut)
async def view_shared_story(
    token: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(SharedStory).where(SharedStory.share_token == token))
    shared = result.scalar_one_or_none()
    if not shared or not shared.is_public:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shared story not found")

    story_result = await db.execute(select(Story).where(Story.id == shared.story_id))
    story = story_result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    kid_result = await db.execute(select(Kid).where(Kid.id == story.kid_id))
    kid = kid_result.scalar_one_or_none()

    shared.view_count += 1
    db.add(shared)

    return SharedStoryOut(
        story_text=story.text,
        story_audio_url=story.audio_url,
        story_theme=story.theme,
        story_language=story.language,
        kid_nickname=kid.nickname if kid else "Unknown",
        share_token=shared.share_token,
    )


@router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_story(
    story_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Story).where(Story.id == uuid.UUID(story_id)))
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    kid_result = await db.execute(select(Kid).where(Kid.id == story.kid_id))
    kid = kid_result.scalar_one_or_none()
    if not kid or kid.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    await db.delete(story)


@router.post("/{story_id}/translate", response_model=StoryTranslationOut)
async def translate(
    story_id: str,
    request: StoryTranslate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Story).where(Story.id == uuid.UUID(story_id)))
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")

    kid_result = await db.execute(select(Kid).where(Kid.id == story.kid_id))
    kid = kid_result.scalar_one_or_none()
    if not kid or kid.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    try:
        translation = await translate_story(db, story, request.target_language)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return StoryTranslationOut.model_validate(translation)
