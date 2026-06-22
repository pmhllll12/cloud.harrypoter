from __future__ import annotations

from abc import ABC, abstractmethod

from harry_poter.app.dtos.dx_sphinx_quiz_dto import SphinxQuizQuery, SphinxQuizResponse


class SphinxQuizPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: SphinxQuizQuery) -> SphinxQuizResponse:
        raise NotImplementedError
