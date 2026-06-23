from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from harry_poter.adapter.inbound.api.schemas.dx_sphinx_quiz_schemas import SphinxQuizSchema
from harry_poter.app.dtos.dx_sphinx_quiz_dto import (
    QuizListItem,
    SphinxQuizResponse,
    SubmitAnswerQuery,
    SubmitAnswerResponse,
)


class SphinxQuizUseCase(ABC):

    @abstractmethod
    async def test_model(self, test_set) -> dict[str, Any]:
        '''스핑크스가 덤블도어가 제안한 모델들의 훈련 정도를 점수화 해서 1등을 뽑는것'''
        pass

    @abstractmethod
    async def introduce_myself(self, schema: SphinxQuizSchema) -> SphinxQuizResponse:
        '''스핑크스 퀴즈의 자기소개 메소드'''
        pass

    @abstractmethod
    async def quiz_search(self, user_id: int, heritage_name: str) -> dict[str, Any]:
        '''정답을 맞히지 않은 문화재 퀴즈 중 하나를 랜덤으로 반환'''
        pass

    @abstractmethod
    async def get_quiz_list(self, user_id: int, heritage_name: str) -> list[QuizListItem]:
        '''문화재 퀴즈 전체 목록을 정답 여부와 함께 반환'''
        pass

    @abstractmethod
    async def submit_answer(self, query: SubmitAnswerQuery) -> SubmitAnswerResponse:
        '''퀴즈 정답 제출 — 정답이면 결과 저장'''
        pass
