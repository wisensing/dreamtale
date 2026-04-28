import uuid
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.user import User
from app.models.kid import Kid
from app.models.story import Story
from app.models.bedtime import BedtimeSession
from app.schemas.bedtime import BedtimeSessionCreate, BedtimeStreak, BedtimeStats
from app.auth.supabase import get_current_user

router = APIRouter(prefix="/bedtime", tags=["bedtime"])


@router.post("/sessions", status_code=status.HTTP_201_CREATED)
async def create_bedtime_session(
    request: BedtimeSessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    kid_result = await db.execute(
        select(Kid).where(Kid.id == uuid.UUID(request.kid_id), Kid.user_id == current_user.id)
    )
    kid = kid_result.scalar_one_or_none()
    if not kid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kid not found")

    session = BedtimeSession(
        kid_id=kid.id,
        date=request.date,
        bedtime_actual=request.bedtime_actual,
        story_id=uuid.UUID(request.story_id) if request.story_id else None,
        duration_minutes=request.duration_minutes,
    )
    db.add(session)
    await db.flush()
    return {"id": str(session.id), "status": "recorded"}


@router.get("/streaks/{kid_id}", response_model=BedtimeStreak)
async def get_streaks(
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
        select(BedtimeSession.date)
        .where(BedtimeSession.kid_id == kid.id)
        .order_by(BedtimeSession.date.desc())
    )
    dates = [row[0] for row in result.all()]

    current_streak = 0
    if dates:
        today = date.today()
        check_date = today
        for d in dates:
            if d == check_date:
                current_streak += 1
                check_date -= timedelta(days=1)
            elif d < check_date:
                break

    longest_streak = 0
    if dates:
        streak = 1
        for i in range(1, len(dates)):
            if dates[i - 1] - dates[i] == timedelta(days=1):
                streak += 1
            else:
                longest_streak = max(longest_streak, streak)
                streak = 1
        longest_streak = max(longest_streak, streak)

    return BedtimeStreak(
        current_streak=current_streak,
        longest_streak=longest_streak,
        last_bedtime_date=dates[0] if dates else None,
    )


@router.get("/stats/{kid_id}", response_model=BedtimeStats)
async def get_stats(
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

    total_result = await db.execute(
        select(func.count()).where(BedtimeSession.kid_id == kid.id)
    )
    total_sessions = total_result.scalar() or 0

    avg_result = await db.execute(
        select(func.avg(BedtimeSession.duration_minutes)).where(BedtimeSession.kid_id == kid.id)
    )
    avg_duration = avg_result.scalar()

    stories_result = await db.execute(
        select(func.count()).where(
            BedtimeSession.kid_id == kid.id,
            BedtimeSession.story_id.isnot(None),
        )
    )
    stories_played = stories_result.scalar() or 0

    streak_data = await get_streaks(kid_id, current_user, db)

    week_ago = date.today() - timedelta(days=7)
    weekly_result = await db.execute(
        select(BedtimeSession)
        .where(BedtimeSession.kid_id == kid.id, BedtimeSession.date >= week_ago)
        .order_by(BedtimeSession.date)
    )
    weekly_sessions = weekly_result.scalars().all()
    weekly_data = [
        {"date": str(s.date), "bedtime": s.bedtime_actual, "duration": s.duration_minutes}
        for s in weekly_sessions
    ]

    return BedtimeStats(
        total_sessions=total_sessions,
        avg_duration_minutes=float(avg_duration) if avg_duration else None,
        stories_played=stories_played,
        streak=streak_data,
        weekly_data=weekly_data,
    )
