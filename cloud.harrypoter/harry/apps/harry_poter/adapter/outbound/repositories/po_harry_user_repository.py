from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from harry_poter.app.dtos.po_harry_user_dto import HarryUserQuery, HarryUserResponse
from harry_poter.app.ports.output.po_harry_user_port import HarryUserPort

logger = logging.getLogger(__name__)


class HarryUserRepository(HarryUserPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: HarryUserQuery) -> HarryUserResponse:
        logger.info("[HarryUserRepository] introduce_myself | request_data=%s", query)
        return HarryUserResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )
