from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from harry_poter.adapter.inbound.api.schemas.sm_dumbledore_store_schemas import DumbledoreStoreSchema
from harry_poter.app.dtos.sm_dumbledore_store_dto import DumbledoreStoreResponse


class DumbledoreStoreStrategy(ABC):
    """생존 예측 알고리즘 전략 인터페이스 (Strategy).

    `_docs/harry-features.md` 의 TOP 10 알고리즘을 각각 구현체로 둔다.
    """

    name: str

    @abstractmethod
    def fit(self, features: Any, target: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def predict(self, features: Any) -> Any:
        raise NotImplementedError


class DumbledoreStoreUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: DumbledoreStoreSchema) -> DumbledoreStoreResponse:
        raise NotImplementedError
