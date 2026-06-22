from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from harry_poter.adapter.inbound.api.schemas.ax_hermione_route_schemas import HermioneRouteSchema
from harry_poter.app.dtos.ax_hermione_route_dto import HermioneRouteResponse


class HermioneRouteUseCase(ABC):

    @abstractmethod
    def analyze_intent(self, question: str) -> dict[str, Any]:
        '''Kiwi 형태소 분석으로 프론트 질문의 의도를 파악하는 추상 메소드'''
        pass

    @abstractmethod
    def extract_champion_profile(self, message: str) -> dict[str, Any]:
        '''생존 예측 질의 문장에서 나이·성별 등 챔피언 프로필을 추출하는 추상 메소드'''
        pass

    @abstractmethod
    async def introduce_myself(self, schema: HermioneRouteSchema) -> HermioneRouteResponse:
        '''헤르미온느 라우트의 자기소개 메소드'''
        pass
