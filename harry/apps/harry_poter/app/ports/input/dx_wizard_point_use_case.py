from __future__ import annotations

import io
from abc import ABC, abstractmethod

from pandas import DataFrame

from harry_poter.adapter.inbound.api.schemas.dx_wizard_point_schemas import WizardPointSchema
from harry_poter.app.dtos.dx_wizard_point_dto import WizardPointResponse


class WizardPointUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: WizardPointSchema) -> WizardPointResponse:
        '''위저드 포인트의 자기소개 메소드'''
        pass

    @abstractmethod
    def generate_correlation_plot(self, dataset: DataFrame) -> io.BytesIO:
        '''생존율 상관관계 히트맵을 PNG 이미지 버퍼로 생성'''
        pass

    @abstractmethod
    def get_survived_correlation_ranking(self, dataset: DataFrame) -> list[tuple[str, float]]:
        '''Survived와의 상관계수를 절댓값 내림차순으로 반환'''
        pass
