from __future__ import annotations

from abc import ABC, abstractmethod

from harry_poter.app.dtos.po_harry_user_dto import HarryUserQuery, HarryUserResponse


class HarryUserPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: HarryUserQuery) -> HarryUserResponse:
        raise NotImplementedError
