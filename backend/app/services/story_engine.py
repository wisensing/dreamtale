import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.story import Story, StoryVersion
from app.models.kid import Kid
from app.services.llm_provider import get_llm_provider
from app.services.tts_provider import get_tts_provider
from app.services.prompt_builder import build_system_prompt, build_user_prompt
from app.services.safety_filter import pre_filter_prompt, post_filter_story, check_tone
from app.services.diversity_tracker import get_recent_themes


async def generate_story(
    db: AsyncSession,
    kid: Kid,
    keywords: str | None = None,
    language: str = "en",
    story_style: str = "",
    chat_session_id: uuid.UUID | None = None,
) -> Story:
    is_safe, reason = pre_filter_prompt(keywords)
    if not is_safe:
        raise ValueError(f"Prompt rejected: {reason}")

    recent_themes = await get_recent_themes(db, str(kid.id))

    system_prompt = build_system_prompt(
        child_name=kid.nickname,
        age=kid.age,
        language=language,
        keywords=keywords,
        story_style=story_style or kid.companion_name or "",
        fears=kid.fears,
        recent_themes=recent_themes,
    )
    user_prompt = build_user_prompt(keywords, kid.nickname, kid.age)

    llm = get_llm_provider()
    story_text = await llm.generate(system_prompt, user_prompt)

    is_safe, safety_score, reason = post_filter_story(story_text)
    if not is_safe:
        raise ValueError(f"Story rejected by safety filter: {reason}")

    tone_ok, tone_reason = check_tone(story_text)
    if not tone_ok:
        story_text += "\n\nAnd so, with a gentle yawn and a peaceful heart, it was time to sleep. Sweet dreams."

    tts = get_tts_provider()
    audio_url = await tts.generate_audio(story_text, language=language)

    age_config = __import__("app.services.age_config", fromlist=["get_age_config"]).get_age_config(kid.age)

    story = Story(
        kid_id=kid.id,
        chat_session_id=chat_session_id,
        text=story_text,
        audio_url=audio_url,
        theme=keywords or "random",
        educational_topic=age_config.educational_focus[0],
        story_style=story_style,
        language=language,
        keywords_used=keywords.split(",") if keywords else [],
        safety_score=safety_score,
    )
    db.add(story)
    await db.flush()

    return story


async def modify_story(
    db: AsyncSession,
    story: Story,
    modification: str,
    kid: Kid,
    language: str | None = None,
) -> Story:
    current_version = 0
    if story.versions:
        current_version = max(v.version_number for v in story.versions)

    version = StoryVersion(
        story_id=story.id,
        text=story.text,
        audio_url=story.audio_url,
        version_number=current_version + 1,
        modification_prompt=modification,
    )
    db.add(version)

    recent_themes = await get_recent_themes(db, str(kid.id))

    system_prompt = build_system_prompt(
        child_name=kid.nickname,
        age=kid.age,
        language=language or story.language,
        keywords=modification,
        story_style=story.story_style,
        fears=kid.fears,
        recent_themes=recent_themes,
    )
    user_prompt = (
        f"Here is the current story:\n\n{story.text}\n\n"
        f"The parent wants this change: {modification}\n\n"
        f"Rewrite the story with this modification. Keep it a bedtime story for {kid.nickname}."
    )

    llm = get_llm_provider()
    new_text = await llm.generate(system_prompt, user_prompt)

    is_safe, safety_score, reason = post_filter_story(new_text)
    if not is_safe:
        raise ValueError(f"Modified story rejected: {reason}")

    target_language = language or story.language
    tts = get_tts_provider()
    audio_url = await tts.generate_audio(new_text, target_language)

    story.text = new_text
    story.audio_url = audio_url
    story.language = target_language
    story.safety_score = safety_score
    db.add(story)
    await db.flush()

    return story


async def translate_story(
    db: AsyncSession,
    story: Story,
    target_language: str,
) -> "StoryTranslation":
    from app.models.story import StoryTranslation

    llm = get_llm_provider()
    system_prompt = (
        f"You are a professional children's story translator. Translate the following bedtime story "
        f"into {target_language}. Keep the tone gentle and calm. Use simple vocabulary suitable for "
        f"children learning this language."
    )
    user_prompt = f"Translate this story:\n\n{story.text}"

    translated_text = await llm.generate(system_prompt, user_prompt)

    tts = get_tts_provider()
    audio_url = await tts.generate_audio(translated_text, target_language)

    translation = StoryTranslation(
        story_id=story.id,
        language=target_language,
        translated_text=translated_text,
        audio_url=audio_url,
    )
    db.add(translation)
    await db.flush()

    return translation
