from __future__ import annotations

import asyncio
from typing import Any

from harry_poter.adapter.inbound.api.schemas.sm_dumbledore_store_schemas import DumbledoreStoreSchema
from harry_poter.app.dtos.sm_dumbledore_store_dto import DumbledoreStoreQuery, DumbledoreStoreResponse
from harry_poter.app.ports.input.sm_dumbledore_store_use_case import DumbledoreStoreStrategy, DumbledoreStoreUseCase
from harry_poter.app.ports.output.sm_dumbledore_store_port import DumbledoreStorePort
from harry_poter.adapter.outbound.orm.sm_dumbledore_store_strategies import (
    LogisticRegressionStrategy,
)


class DumbledoreStoreInteractor(DumbledoreStoreUseCase):
    def __init__(
        self,
        repository: DumbledoreStorePort,
        strategy: DumbledoreStoreStrategy | None = None,
    ) -> None:
        self.repository = repository
        self.strategy: DumbledoreStoreStrategy = strategy or LogisticRegressionStrategy()

    def set_strategy(self, strategy: DumbledoreStoreStrategy) -> None:
        """베이스라인(Logistic Regression)에서 다른 알고리즘으로 교체할 때 사용."""
        self.strategy = strategy

    async def train(self, features: Any, target: Any) -> None:
        await asyncio.to_thread(self.strategy.fit, features, target)

    async def predict(self, features: Any) -> Any:
        return await asyncio.to_thread(self.strategy.predict, features)

    async def introduce_myself(self, schema: DumbledoreStoreSchema) -> DumbledoreStoreResponse:
        query = DumbledoreStoreQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)
