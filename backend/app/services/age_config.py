from dataclasses import dataclass


@dataclass
class AgeConfig:
    target_words: int
    vocabulary_level: str
    themes: list[str]
    educational_focus: list[str]
    settings: list[str]


AGE_CONFIGS: dict[tuple[int, int], AgeConfig] = {
    (2, 3): AgeConfig(
        target_words=100,
        vocabulary_level="Simple, repetitive",
        themes=["animals", "colors", "family", "toys", "food"],
        educational_focus=["counting", "emotions", "routines", "hygiene"],
        settings=["home", "garden", "playground", "bathroom"],
    ),
    (4, 5): AgeConfig(
        target_words=150,
        vocabulary_level="Basic + new words",
        themes=["friendship", "nature", "animals", "seasons", "vehicles"],
        educational_focus=["sharing", "kindness", "basic safety", "seasons", "weather"],
        settings=["park", "forest", "beach", "school", "farm"],
    ),
    (6, 7): AgeConfig(
        target_words=200,
        vocabulary_level="Elementary",
        themes=["courage", "discovery", "teamwork", "magic", "space"],
        educational_focus=["emergency skills", "basic math", "recycling", "empathy", "science"],
        settings=["enchanted forest", "castle", "mountain", "ocean", "laboratory"],
    ),
    (8, 10): AgeConfig(
        target_words=250,
        vocabulary_level="Intermediate",
        themes=["mystery", "space", "history", "adventure", "invention"],
        educational_focus=["critical thinking", "problem-solving", "money basics", "geography", "science concepts"],
        settings=["ancient ruins", "space station", "underground cave", "museum", "inventor's workshop"],
    ),
}


def get_age_config(age: int) -> AgeConfig:
    for (low, high), config in AGE_CONFIGS.items():
        if low <= age <= high:
            return config
    return AGE_CONFIGS[(4, 5)]
