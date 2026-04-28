from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.story import Story


async def get_recent_themes(db: AsyncSession, kid_id: str, limit: int = 10) -> list[str]:
    result = await db.execute(
        select(Story.theme)
        .where(Story.kid_id == kid_id)
        .order_by(Story.created_at.desc())
        .limit(limit)
    )
    return [row[0] for row in result.all() if row[0]]


async def get_recent_educational_topics(db: AsyncSession, kid_id: str, limit: int = 10) -> list[str]:
    result = await db.execute(
        select(Story.educational_topic)
        .where(Story.kid_id == kid_id)
        .order_by(Story.created_at.desc())
        .limit(limit)
    )
    return [row[0] for row in result.all() if row[0]]
