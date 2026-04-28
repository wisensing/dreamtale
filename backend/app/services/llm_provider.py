from abc import ABC, abstractmethod
from typing import Optional
import random


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 500) -> str:
        ...


class MockLLMProvider(BaseLLMProvider):
    TEMPLATES = {
        "2-3": [
            "Once upon a time, little {name} saw a {animal} in the garden. The {animal} was {color} and very friendly. "
            "\"Hello, {name}!\" said the {animal}. \"Let's count the flowers!\" One, two, three! {name} counted three "
            "beautiful flowers. The {animal} smiled. \"You are so good at counting, {name}!\" Then the sun began to set, "
            "and the {animal} said, \"Time to rest, little one. Close your eyes and dream of more flowers tomorrow.\" "
            "{name} yawned, feeling warm and happy. Goodnight, {name}. Goodnight, {animal}. Goodnight, world.",

            "{name} had a very special friend — a tiny {animal} who lived in a {place}. Every night before bed, the "
            "{animal} would visit {name} and say, \"Let's brush our teeth together!\" So {name} and the {animal} "
            "brushed their teeth: up and down, round and round. Then the {animal} said, \"Now let's wash our hands!\" "
            "Splash, splash, splash went the water. {name} giggled. \"You're so clean!\" said the {animal}. "
            "\"Now it's time for bed, {name}. Clean hands, clean teeth, sweet dreams.\" {name} snuggled under the "
            "blankets, feeling cozy and fresh. The {animal} whispered, \"Goodnight, {name}. I'll see you tomorrow.\"",

            "The moon was big and round outside {name}'s window. \"Look at the moon!\" said {name}'s {animal}. "
            "\"It looks like a big round cookie!\" {name} laughed. \"Can we eat it?\" \"No, no!\" said the {animal}. "
            "\"But we can wave to it!\" So {name} waved at the moon, and the moon seemed to smile back. "
            "\"The moon watches over you, {name},\" said the {animal}. \"It keeps you safe all night long.\" "
            "{name} felt safe and warm. \"Goodnight, moon,\" whispered {name}. \"Goodnight, {name},\" whispered the moon.",
        ],
        "4-5": [
            "One sunny morning, {name} and their friend the {animal} decided to go on an adventure to the {place}. "
            "Along the way, they met a little bird who couldn't find its way home. \"Don't worry!\" said {name}. "
            "\"We'll help you!\" The {animal} said, \"We should always help our friends — that's what kindness means.\" "
            "{name} and the {animal} walked with the bird until they found its tree. \"Thank you, {name}!\" chirped "
            "the bird. \"You taught me that friends help each other.\" {name} smiled and felt warm inside. When {name} "
            "got home, the {animal} said, \"You were very kind today, {name}. Kindness makes the world brighter.\" "
            "That night, {name} drifted off to sleep, dreaming of helping more friends tomorrow.",

            "{name} was playing in the {place} when they found something amazing — a box of colorful crayons! "
            "\"Let's draw!\" said the {animal}. {name} drew a big rainbow with all the colors: red, orange, yellow, "
            "green, blue, and purple. \"I love sharing my crayons!\" {name} said. Just then, a little friend came by. "
            "\"Can I draw too?\" they asked. \"Of course!\" said {name}. \"Sharing makes everything more fun.\" "
            "They drew together — houses, flowers, and a big happy sun. The {animal} smiled. \"You know, {name}, "
            "when we share, everyone gets to have a good time.\" That night, {name} dreamed of a world where everyone "
            "shared and played together. Sweet dreams, {name}.",

            "It was a rainy day, and {name} was looking out the window. \"I wish I could play outside,\" sighed {name}. "
            "But the {animal} had an idea! \"Rain is wonderful, {name}! Did you know that rain helps flowers grow and "
            "fills up the rivers?\" {name} watched the raindrops race down the window. \"One, two, three drops!\" "
            "counted {name}. The {animal} said, \"You know what's important on a rainy day? Holding a grown-up's hand "
            "when you cross the street, because the road can be slippery!\" {name} nodded. \"I'll always hold hands!\" "
            "The rain made a gentle pitter-patter sound, like a lullaby. {name} yawned. \"Rain isn't so bad,\" "
            "whispered {name}. \"It's like the sky is singing me to sleep.\"",
        ],
        "6-7": [
            "{name} and the {animal} were exploring the {place} when they heard a strange sound. \"What's that?\" "
            "asked {name}. It was a little fox who had gotten a small scrape on its paw. \"Oh no!\" said {name}. "
            "\"Are you okay?\" The {animal} said, \"{name}, do you know what to do if someone gets hurt? First, you "
            "stay calm. Then you find a grown-up you trust. And if it's a big emergency, you call 911.\" {name} "
            "nodded and helped the fox find its way to a safe place. \"Thank you, {name}\" said the fox. \"You were "
            "so brave and knew just what to do!\" {name} felt proud. That night, as the stars twinkled outside, "
            "{name} whispered, \"I know how to keep people safe now.\" The {animal} snuggled close. \"You're growing "
            "up so wise, {name}. Sweet dreams.\"",

            "{name} woke up to a beautiful morning and decided to build the tallest tower ever! Using blocks, {name} "
            "stacked: one, two, three, four, five, six! The tower was so tall! But then — CRASH — it fell down. "
            "\"Oh no!\" said {name}. The {animal} smiled. \"That's okay, {name}. Did you know that scientists try "
            "things many times before they get it right? Each time you try, you learn something new!\" {name} thought "
            "about it. \"You're right! Let me try again!\" This time, {name} made the base wider. One, two, three... "
            "ten blocks high! It stood tall and strong! \"I did it!\" cheered {name}. The {animal} said, \"That's "
            "the spirit, {name}! Trying again is how we learn and grow.\" That night, {name} dreamed of building "
            "amazing things, one block at a time.",

            "In the magical {place}, {name} discovered a garden where the flowers could talk! \"Hello, {name}!\" said "
            "a bright sunflower. \"Did you know that we flowers need three things to grow? Sun, water, and good soil!\" "
            "{name} was amazed. \"That's like how I need food, water, and sleep to grow!\" \"Exactly!\" said the "
            "sunflower. The {animal} added, \"And did you know that plants help clean the air we breathe? That's why "
            "it's important to take care of nature.\" {name} watered the garden carefully and promised to always take "
            "care of the earth. As the sun set over the garden, the flowers sang a gentle lullaby. {name} felt the "
            "warm earth beneath and the cool breeze above. \"Thank you, garden friends,\" whispered {name}. "
            "Sleep well, {name}. Tomorrow is a new day to grow.",
        ],
        "8-10": [
            "{name} had always wondered what lay beyond the {place}. One evening, the {animal} appeared with a map. "
            "\"Ready for an adventure?\" it asked. Together, they traveled through a forest of whispering trees and "
            "across a bridge made of moonlight. At the center of the bridge was a riddle: \"I have cities but no "
            "houses, forests but no trees, and water but no fish. What am I?\" {name} thought carefully. \"A map!\" "
            "\"Correct!\" said the bridge keeper. The {animal} smiled. \"{name}, did you know that maps have been used "
            "for thousands of years? Ancient explorers mapped the stars to find their way across oceans.\" {name} "
            "gazed at the sky. The stars looked like their very own map. As they crossed the bridge, {name} felt brave "
            "and curious. That night, back in their own cozy bed, {name} traced imaginary maps on the ceiling, "
            "dreaming of all the places yet to explore. The {animal} whispered, \"The greatest adventure, {name}, "
            "is the one that begins in your mind.\"",

            "Professor {animal} welcomed {name} to the Science Lab of Wonders! \"Today's experiment: making a rainbow!\" "
            "{name} filled a glass with water and placed it in the sunlight. A beautiful rainbow appeared on the wall! "
            "\"How does it work?\" asked {name}. \"White light is actually made of all the colors of the rainbow!\" "
            "explained the {animal}. \"When light passes through water, it bends and separates into different colors — "
            "that's called refraction.\" {name} was fascinated. \"So rainbows after rain are made the same way?\" "
            "\"Exactly! Water droplets in the air act like tiny prisms!\" {name} drew the experiment in a notebook. "
            "\"Science is amazing!\" The {animal} nodded. \"And the best scientists ask questions, just like you, "
            "{name}.\" As the lab grew quiet, {name} looked at the rainbow on the wall one last time. The colors "
            "seemed to whisper, \"Goodnight, scientist.\" {name} smiled and closed their eyes.",

            "{name} stood at the edge of the {place}, looking at two paths. The {animal} appeared beside them. "
            "\"Which way?\" it asked. \"I don't know,\" said {name}. \"What if I choose wrong?\" The {animal} smiled. "
            "\"There's something I want to teach you, {name}. It's called critical thinking. Before you decide, ask "
            "yourself: What do I know? What could happen? What makes sense?\" {name} looked down both paths. The left "
            "path was bright and easy. The right path was darker but had footprints — someone had been there before. "
            "\"The right path has footprints, so it must be safe. And sometimes the harder path leads to the best "
            "discoveries!\" {name} chose the right path and found a hidden waterfall, sparkling like diamonds. "
            "\"You used your thinking skills, {name}!\" said the {animal}. That night, {name} realized that the best "
            "choices come from thinking carefully and being brave. Sweet dreams, {name}. Tomorrow, you'll think and "
            "choose and grow even more.",
        ],
    }

    ANIMALS = [
        "gentle bear", "wise owl", "friendly rabbit", "playful fox",
        "kind deer", "curious squirrel", "cheerful frog", "brave little mouse",
    ]
    COLORS = ["red", "blue", "green", "yellow", "purple", "orange", "pink"]
    PLACES = [
        "enchanted forest", "magical garden", "sparkling meadow",
        "cozy cottage", "starry hilltop", "sunny beach", "rainbow valley",
    ]

    async def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 500) -> str:
        age_group = self._extract_age_group(system_prompt)
        child_name = self._extract_field(system_prompt, "child_name") or "little one"
        templates = self.TEMPLATES.get(age_group, self.TEMPLATES["4-5"])
        template = random.choice(templates)

        animal = random.choice(self.ANIMALS)
        color = random.choice(self.COLORS)
        place = random.choice(self.PLACES)

        story = template.format(name=child_name, animal=animal, color=color, place=place)
        return story

    def _extract_age_group(self, prompt: str) -> str:
        try:
            age = int(prompt.split("Age-appropriate for")[1].split("years")[0].strip())
            if age <= 3:
                return "2-3"
            elif age <= 5:
                return "4-5"
            elif age <= 7:
                return "6-7"
            else:
                return "8-10"
        except (IndexError, ValueError):
            return "4-5"

    def _extract_field(self, prompt: str, field_name: str) -> str | None:
        try:
            marker = f'"{field_name}"' if field_name == "child_name" else field_name
            return None
        except (IndexError, ValueError):
            return None


class OpenAILLMProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    async def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 500) -> str:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=self.api_key)
        response = await client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.8,
        )
        return response.choices[0].message.content


class OpenRouterLLMProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "qwen/qwen-2.5-72b-instruct"):
        self.api_key = api_key
        self.model = model

    async def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 500) -> str:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=self.api_key, base_url="https://openrouter.ai/api/v1")
        response = await client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.8,
        )
        return response.choices[0].message.content


def get_llm_provider() -> BaseLLMProvider:
    from app.config import get_settings
    settings = get_settings()

    if settings.LLM_PROVIDER == "openai":
        return OpenAILLMProvider(settings.OPENAI_API_KEY)
    elif settings.LLM_PROVIDER == "openrouter":
        return OpenRouterLLMProvider(settings.OPENROUTER_API_KEY)
    else:
        return MockLLMProvider()
