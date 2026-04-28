from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "DreamTale"
    DEBUG: bool = False
    API_PREFIX: str = "/api"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://dreamtale:dreamtale@localhost:5432/dreamtale"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_10_CREDITS: str = ""
    STRIPE_PRICE_25_CREDITS: str = ""
    STRIPE_PRICE_50_CREDITS: str = ""
    STRIPE_PRICE_100_CREDITS: str = ""
    STRIPE_PREMIUM_MONTHLY: str = ""
    STRIPE_FAMILY_MONTHLY: str = ""

    # LLM Provider: "mock" | "openai" | "openrouter" | "vllm"
    LLM_PROVIDER: str = "mock"
    OPENAI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    VLLM_BASE_URL: str = ""

    # TTS Provider: "mock" | "google" | "elevenlabs"
    TTS_PROVIDER: str = "mock"
    GOOGLE_TTS_CREDENTIALS: str = ""
    ELEVENLABS_API_KEY: str = ""

    # Audio storage
    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY: str = ""
    R2_SECRET_KEY: str = ""
    R2_BUCKET: str = "dreamtale-audio"

    # Encryption key for kid nicknames (Fernet)
    ENCRYPTION_KEY: str = ""

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8081"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
