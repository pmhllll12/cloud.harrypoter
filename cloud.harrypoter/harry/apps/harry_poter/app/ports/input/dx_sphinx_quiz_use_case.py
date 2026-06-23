from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from harry_poter.adapter.inbound.api.schemas.dx_sphinx_quiz_schemas import SphinxQuizSchema
from harry_poter.app.dtos.dx_sphinx_quiz_dto import SphinxQuizResponse


class SphinxQuizUseCase(ABC):

    @abstractmethod
    async def test_model(self, test_set) -> dict[str, Any]:
        '''스핑크스가 덤블도어가 제안한 모델들의 훈련 정도를 점수화 해서 1등을 뽑는것'''
        pass

    @abstractmethod
    async def introduce_myself(self, schema: SphinxQuizSchema) -> SphinxQuizResponse:
        '''스핑크스 퀴즈의 자기소개 메소드'''
        pass
