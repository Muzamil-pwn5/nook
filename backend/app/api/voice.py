import os

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

router = APIRouter(prefix="/agent", tags=["Agent voice"])


class SpeakRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1200)
    voice_id: str | None = Field(default=None, max_length=120)


@router.post("/speak", response_class=Response)
async def speak(request: SpeakRequest):
    """Turn a short agent response into audio without exposing the API key."""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="ElevenLabs is not configured for this environment.",
        )

    voice_id = request.voice_id or os.getenv(
        "ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL"
    )
    model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            result = await client.post(
                url,
                headers={
                    "xi-api-key": api_key,
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                },
                json={
                    "text": request.text,
                    "model_id": model_id,
                    "voice_settings": {
                        "stability": 0.48,
                        "similarity_boost": 0.78,
                        "style": 0.18,
                        "use_speaker_boost": True,
                    },
                },
            )
    except httpx.HTTPError as error:
        raise HTTPException(status_code=502, detail="ElevenLabs request failed.") from error

    if not result.is_success:
        raise HTTPException(
            status_code=502,
            detail="ElevenLabs could not generate audio for this response.",
        )
    return Response(content=result.content, media_type="audio/mpeg")
