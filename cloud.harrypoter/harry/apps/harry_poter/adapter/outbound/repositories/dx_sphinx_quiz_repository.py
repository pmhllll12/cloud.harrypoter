from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from harry_poter.app.dtos.dx_sphinx_quiz_dto import SphinxQuizQuery, SphinxQuizResponse
from harry_poter.app.ports.output.dx_sphinx_quiz_port import SphinxQuizPort

logger = logging.getLogger(__name__)


class SphinxQuizRepository(SphinxQuizPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: SphinxQuizQuery) -> SphinxQuizResponse:
        logger.info("[SphinxQuizRepository] introduce_myself | request_data=%s", query)
        return SphinxQuizResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )
