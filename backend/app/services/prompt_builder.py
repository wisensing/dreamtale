import random
from app.services.age_config import get_age_config


SYSTEM_TEMPLATE = """You are a gentle children's storyteller for bedtime.

RULES:
- Exactly {target_words} words (±10%)
- Age-appropriate for {age} years old
- Use child's name "{child_name}" naturally, 2-3 times
- Calm, soothing tone — ending must encourage sleep
- EDUCATIONAL GOAL: Naturally teach about {educational_theme} through the story
- Language: {language}
- Story style inspiration: {story_style}
- AVOID: {fears_to_avoid}
- AVOID recent themes: {recent_themes}

Parent's keywords for today: {keywords}
If no keywords provided, choose a creative theme from: {theme} | {setting}

Lesson: {lesson}
"""


def build_system_prompt(
    child_name: str,
    age: int,
    language: str = "en",
    keywords: str | None = None,
    story_style: str = "",
    fears: list[str] | None = None,
    recent_themes: list[str] | None = None,
) -> str:
    config = get_age_config(age)

    educational_themes = config.educational_focus
    educational_theme = random.choice(educational_themes)

    theme = random.choice(config.themes)
    setting = random.choice(config.settings)

    lessons = [
        "It's important to always try your best, even when things are hard.",
        "Being kind to others makes the world a better place.",
        "Listening to your grown-ups helps keep you safe.",
        "Trying new things can be scary but also wonderful.",
        "Sharing with friends makes everything more fun.",
        "It's okay to ask for help when you need it.",
        "Being brave doesn't mean you're never scared.",
        "Taking care of yourself — like brushing teeth and washing hands — is important.",
    ]
    lesson = random.choice(lessons)

    fears_str = ", ".join(fears) if fears else "nothing specific"
    recent_str = ", ".join(recent_themes) if recent_themes else "none"
    keywords_str = keywords if keywords else "(none — choose your own creative theme)"

    return SYSTEM_TEMPLATE.format(
        target_words=config.target_words,
        age=age,
        child_name=child_name,
        educational_theme=educational_theme,
        language=language,
        story_style=story_style or "calm and gentle like a lullaby",
        fears_to_avoid=fears_str,
        recent_themes=recent_str,
        keywords=keywords_str,
        theme=theme,
        setting=setting,
        lesson=lesson,
    )


def build_user_prompt(keywords: str | None, child_name: str, age: int) -> str:
    if keywords:
        return f"Tell a bedtime story about: {keywords}. The child's name is {child_name} and they are {age} years old."
    return f"Tell a bedtime story for {child_name}, who is {age} years old. Surprise them with a creative theme!"
