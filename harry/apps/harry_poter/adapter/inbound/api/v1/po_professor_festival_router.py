import logging

from fastapi import APIRouter, Depends

from harry_poter.adapter.inbound.api.schemas.po_professor_festival_schemas import (
    ProfessorFestivalSchema,
    ProfessorFestivalChatRequest,
    ProfessorFestivalChatResponse,
)
from harry_poter.app.dtos.po_professor_festival_dto import ProfessorFestivalResponse
from harry_poter.app.ports.input.po_professor_festival_use_case import ProfessorFestivalUseCase
from harry_poter.dependencies.po_professor_festival_provider import get_professor_festival_use_case

logger = logging.getLogger(__name__)

professor_festival_router = APIRouter(prefix="/professor", tags=["professor"])


@professor_festival_router.post("/chat", response_model=ProfessorFestivalChatResponse)
async def professor_festival_chat(
    schema: ProfessorFestivalChatRequest,
    professor: ProfessorFestivalUseCase = Depends(get_professor_festival_use_case),
) -> ProfessorFestivalChatResponse:
    logger.info(f"[professor/chat] message={schema.message}")
    return await professor.chat(schema)


@professor_festival_router.get("/myself")
async def introduce_myself(
    professor: ProfessorFestivalUseCase = Depends(get_professor_festival_use_case),
) -> ProfessorFestivalResponse:
    return await professor.introduce_myself(
        ProfessorFestivalSchema(
            id=0,
            name="덤블도어 교수 (Professor Albus Dumbledore)",
        )
    )
