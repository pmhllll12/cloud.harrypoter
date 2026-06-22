from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from harry_poter.app.dtos.sm_dumbledore_store_dto import DumbledoreStoreQuery, DumbledoreStoreResponse
from harry_poter.app.ports.output.sm_dumbledore_store_port import DumbledoreStorePort

logger = logging.getLogger(__name__)


class DumbledoreStoreRepository(DumbledoreStorePort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: DumbledoreStoreQuery) -> DumbledoreStoreResponse:
        logger.info("[DumbledoreStoreRepository] introduce_myself | request_data=%s", query)
        return DumbledoreStoreResponse(id=query.id, name=query.name)
