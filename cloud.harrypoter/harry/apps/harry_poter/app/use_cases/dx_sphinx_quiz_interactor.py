from __future__ import annotations

import logging
from typing import Any

from harry_poter.adapter.inbound.api.schemas.dx_sphinx_quiz_schemas import SphinxQuizSchema
from harry_poter.app.dtos.dx_sphinx_quiz_dto import SphinxQuizQuery, SphinxQuizResponse
from harry_poter.app.ports.input.dx_sphinx_quiz_use_case import SphinxQuizUseCase
from harry_poter.app.ports.input.po_harry_user_use_case import HarryUserUseCase
from harry_poter.app.ports.output.dx_sphinx_quiz_port import SphinxQuizPort

logger = logging.getLogger(__name__)


class SphinxQuizInteractor(SphinxQuizUseCase):

    def __init__(self, repository: SphinxQuizPort, harry: HarryUserUseCase) -> None:
        self.repository = repository
        self.harry = harry

    async def test_model(self, test_set) -> dict[str, Any]:
        """스핑크스가 덤블도어가 제안한 10개 모델의 트레이닝 정도를 점수화 해서 1등을 뽑는것"""

        train_result = await self.harry.train_model(test_set)
        scores = train_result["scores"]

        ranking = []
        for name in scores:
            ranking.append({"model": name, "accuracy": scores[name]})
        ranking.sort(key=lambda entry: entry["accuracy"], reverse=True)

        rank = 1
        for entry in ranking:
            entry["rank"] = rank
            rank = rank + 1

        winner = ranking[0]["model"]
        logger.info("[SphinxQuizInteractor/test_model] ranking=%s winner=%s", ranking, winner)

        return {"ranking": ranking, "winner": winner}

    async def introduce_myself(self, schema: SphinxQuizSchema) -> SphinxQuizResponse:
        query = SphinxQuizQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)
