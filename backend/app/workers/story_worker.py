from celery import Celery
from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "dreamtale",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task
def generate_story_task(story_id: str) -> dict:
    """Async story generation task (for future use with real LLM)."""
    # This will be implemented when switching to a real LLM provider
    # that takes 10-15 seconds per story
    return {"story_id": story_id, "status": "completed"}
