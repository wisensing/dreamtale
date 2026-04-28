BLOCKED_KEYWORDS = [
    "violence", "kill", "murder", "death", "blood", "weapon", "gun",
    "knife", "drug", "alcohol", "smoke", "scary", "horror", "ghost",
    "demon", "devil", "hell", "curse", "suicide", "abuse", "torture",
]

EXCITING_WORDS = [
    "scream", "shout", "explosion", "chase", "attack", "fight",
    "danger", "emergency", "panic", "terrifying", "nightmare",
]


def pre_filter_prompt(keywords: str | None) -> tuple[bool, str]:
    if not keywords:
        return True, ""
    keywords_lower = keywords.lower()
    for word in BLOCKED_KEYWORDS:
        if word in keywords_lower:
            return False, f"The keyword '{word}' is not allowed in children's stories."
    return True, ""


def post_filter_story(text: str) -> tuple[bool, float, str]:
    text_lower = text.lower()
    for word in BLOCKED_KEYWORDS:
        if word in text_lower:
            return False, 0.0, f"Story contains inappropriate word: '{word}'"

    excitement_count = sum(1 for word in EXCITING_WORDS if word in text_lower)
    if excitement_count > 2:
        return False, 0.5, "Story is too exciting for bedtime."

    safety_score = max(0.0, 1.0 - (excitement_count * 0.15))
    return True, safety_score, ""


def check_tone(text: str) -> tuple[bool, str]:
    has_calm_ending = any(
        word in text.lower()[-200:]
        for word in ["goodnight", "sweet dreams", "sleep", "dream", "rest", "cozy", "peaceful"]
    )
    if not has_calm_ending:
        return False, "Story does not end with a calm, sleep-encouraging tone."
    return True, ""
