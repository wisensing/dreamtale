from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="DreamTale API",
    description="AI Bedtime Story App for Kids",
    version="0.1.0",
    lifespan=lifespan,
)

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import auth, kids, stories, chat, credits, bedtime, tts

app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(kids.router, prefix=settings.API_PREFIX)
app.include_router(stories.router, prefix=settings.API_PREFIX)
app.include_router(chat.router, prefix=settings.API_PREFIX)
app.include_router(credits.router, prefix=settings.API_PREFIX)
app.include_router(bedtime.router, prefix=settings.API_PREFIX)
app.include_router(tts.router, prefix=settings.API_PREFIX)


@app.get("/health")
async def health():
    return {"status": "ok", "app": "DreamTale"}
