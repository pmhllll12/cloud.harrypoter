import os
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv(".env.local")

logger = logging.getLogger(__name__)

tourism_chat_router = APIRouter(prefix="/tourism", tags=["tourism"])

_MODEL = "gemini-2.0-flash"
_SYSTEM_PROMPT = (
    "당신은 대한민국 관광 AI 가이드입니다. "
    "전국의 문화유산, 관광지, 맛집, 교통 정보를 친절하고 상세하게 안내합니다. "
    "답변은 한국어로, 핵심을 간결하게 전달하세요."
)


def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY가 설정되지 않았습니다.")
    return genai.Client(api_key=api_key)


class TourismChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class TourismChatResponse(BaseModel):
    reply: str
    model: str


@tourism_chat_router.post("/chat", response_model=TourismChatResponse)
async def tourism_chat(body: TourismChatRequest) -> TourismChatResponse:
    logger.info("[tourism/chat] message=%s", body.message[:60])
    try:
        client = _get_client()
        response = client.models.generate_content(
            model=_MODEL,
            contents=body.message,
            config=types.GenerateContentConfig(
                system_instruction=_SYSTEM_PROMPT,
            ),
        )
        reply = response.text.strip() if response.text else "응답을 생성하지 못했습니다."
        return TourismChatResponse(reply=reply, model=_MODEL)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("[tourism/chat] error: %s", e)
        raise HTTPException(status_code=500, detail=f"AI 응답 오류: {e}") from e
