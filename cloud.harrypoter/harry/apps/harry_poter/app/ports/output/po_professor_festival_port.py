from __future__ import annotations

from abc import ABC, abstractmethod

from harry_poter.app.dtos.po_professor_festival_dto import ProfessorFestivalQuery, ProfessorFestivalResponse


class ProfessorFestivalPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: ProfessorFestivalQuery) -> ProfessorFestivalResponse:
        raise NotImplementedError
