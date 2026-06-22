from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from harry_poter.app.dtos.ax_lovegood_course_dto import LovegoodCourseQuery, LovegoodCourseResponse
from harry_poter.app.ports.output.ax_lovegood_course_port import LovegoodCoursePort

logger = logging.getLogger(__name__)


class LovegoodCourseRepository(LovegoodCoursePort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: LovegoodCourseQuery) -> LovegoodCourseResponse:
        logger.info("[LovegoodCourseRepository] introduce_myself | request_data=%s", query)
        return LovegoodCourseResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )
