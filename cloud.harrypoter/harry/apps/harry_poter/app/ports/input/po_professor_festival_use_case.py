from __future__ import annotations

from abc import ABC, abstractmethod

from harry_poter.adapter.inbound.api.schemas.po_professor_festival_schemas import (
    ProfessorFestivalSchema,
    ProfessorFestivalChatRequest,
    ProfessorFestivalChatResponse,
)
from harry_poter.app.dtos.po_professor_festival_dto import ProfessorFestivalResponse


class ProfessorFestivalUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: ProfessorFestivalSchema) -> ProfessorFestivalResponse:
        """교수(페스티벌)의 자기소개 메소드"""
        pass

    @abstractmethod
    async def chat(self, body: ProfessorFestivalChatRequest) -> ProfessorFestivalChatResponse:
        """사용자 자연어 입력을 받아 트라이위저드 시합 해설 응답을 반환합니다."""
        pass
