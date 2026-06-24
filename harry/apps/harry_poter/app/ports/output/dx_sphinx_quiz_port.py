from __future__ import annotations

from abc import ABC, abstractmethod

from harry_poter.app.dtos.dx_sphinx_quiz_dto import (
    HeritageQuizItem,
    SphinxQuizQuery,
    SphinxQuizResponse,
)


class SphinxQuizPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: SphinxQuizQuery) -> SphinxQuizResponse:
        raise NotImplementedError

    @abstractmethod
    async def search_heritage(self, keyword: str) -> SphinxQuizResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_quizzes_by_heritage(self, heritage_name: str) -> list[HeritageQuizItem]:
        raise NotImplementedError

    @abstractmethod
    async def get_quiz_by_id(self, quiz_id: int) -> HeritageQuizItem:
        raise NotImplementedError

    @abstractmethod
    async def get_user_progress(self, user_id: int, heritage_name: str) -> list[int]:
        raise NotImplementedError

    @abstractmethod
    async def save_quiz_result(self, user_id: int, quiz_id: int, is_correct: bool) -> None:
        raise NotImplementedError
