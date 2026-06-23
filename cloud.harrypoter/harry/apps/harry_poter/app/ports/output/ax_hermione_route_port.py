from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from harry_poter.app.dtos.ax_hermione_route_dto import HermioneRouteQuery, HermioneRouteResponse


class HermioneRoutePort(ABC):

    @abstractmethod
    def analyze_intent(self, question: str) -> dict[str, Any]:
        '''Kiwi 형태소 분석으로 질문 의도를 파악하는 추상 메소드'''
        pass

    @abstractmethod
    def introduce_myself(self, query: HermioneRouteQuery) -> HermioneRouteResponse:
        '''헤르미온느 라우트의 자기 소개 레포지토리 추상 메소드'''
        pass
