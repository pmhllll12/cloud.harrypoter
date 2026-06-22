from __future__ import annotations

from abc import ABC, abstractmethod

from harry_poter.app.dtos.sm_dumbledore_store_dto import DumbledoreStoreQuery, DumbledoreStoreResponse


class DumbledoreStorePort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: DumbledoreStoreQuery) -> DumbledoreStoreResponse:
        raise NotImplementedError
