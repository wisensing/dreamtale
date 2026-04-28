from pydantic import BaseModel
from datetime import date
from typing import Optional


class BedtimeSessionCreate(BaseModel):
    kid_id: str
    date: date
    bedtime_actual: str
    story_id: Optional[str] = None
    duration_minutes: Optional[int] = None


class BedtimeStreak(BaseModel):
    current_streak: int
    longest_streak: int
    last_bedtime_date: Optional[date]


class BedtimeStats(BaseModel):
    total_sessions: int
    avg_duration_minutes: Optional[float]
    stories_played: int
    streak: BedtimeStreak
    weekly_data: list[dict]
