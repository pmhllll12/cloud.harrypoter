from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from harry_poter.app.dtos.po_professor_festival_dto import ProfessorFestivalQuery, ProfessorFestivalResponse
from harry_poter.app.ports.output.po_professor_festival_port import ProfessorFestivalPort

logger = logging.getLogger(__name__)


class ProfessorFestivalRepository(ProfessorFestivalPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: ProfessorFestivalQuery) -> ProfessorFestivalResponse:
        logger.info("[ProfessorFestivalRepository] introduce_myself | request_data=%s", query)
        return ProfessorFestivalResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )
