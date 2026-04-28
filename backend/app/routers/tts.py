from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from app.models.user import User
from app.auth.supabase import get_current_user
from app.services.tts_provider import get_tts_provider

router = APIRouter(prefix="/tts", tags=["tts"])


class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    voice_id: Optional[str] = None


class TTSResponse(BaseModel):
    audio_url: str


@router.post("/generate", response_model=TTSResponse)
async def generate_tts(
    request: TTSRequest,
    current_user: User = Depends(get_current_user),
):
    tts = get_tts_provider()
    try:
        audio_url = await tts.generate_audio(request.text, request.language, request.voice_id)
    except NotImplementedError as e:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(e))

    return TTSResponse(audio_url=audio_url)
