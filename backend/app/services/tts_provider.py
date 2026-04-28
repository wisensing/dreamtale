from abc import ABC, abstractmethod
from typing import Optional


class BaseTTSProvider(ABC):
    @abstractmethod
    async def generate_audio(self, text: str, language: str = "en", voice_id: Optional[str] = None) -> str:
        """Generate audio from text. Returns a URL to the audio file."""
        ...


class MockTTSProvider(BaseTTSProvider):
    async def generate_audio(self, text: str, language: str = "en", voice_id: Optional[str] = None) -> str:
        return f"https://mock-tts.dreamtale.app/audio/mock_{hash(text) % 10000}.mp3"


class GoogleTTSProvider(BaseTTSProvider):
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path

    async def generate_audio(self, text: str, language: str = "en", voice_id: Optional[str] = None) -> str:
        # Placeholder — implement with google-cloud-texttospeech
        raise NotImplementedError("Google TTS not yet implemented")


class ElevenLabsTTSProvider(BaseTTSProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate_audio(self, text: str, language: str = "en", voice_id: Optional[str] = None) -> str:
        # Placeholder — implement with ElevenLabs API
        raise NotImplementedError("ElevenLabs TTS not yet implemented")


def get_tts_provider() -> BaseTTSProvider:
    from app.config import get_settings
    settings = get_settings()

    if settings.TTS_PROVIDER == "google":
        return GoogleTTSProvider(settings.GOOGLE_TTS_CREDENTIALS)
    elif settings.TTS_PROVIDER == "elevenlabs":
        return ElevenLabsTTSProvider(settings.ELEVENLABS_API_KEY)
    else:
        return MockTTSProvider()
