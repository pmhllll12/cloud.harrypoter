from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from harry_poter.adapter.inbound.api.schemas.po_harry_user_schemas import HarryUserSchema
from harry_poter.app.dtos.po_harry_user_dto import HarryUserResponse


class HarryUserUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: HarryUserSchema) -> HarryUserResponse:
        """해리(유저) 자기소개."""
        raise NotImplementedError

    @abstractmethod
    async def train_model(self, train_set) -> dict[str, Any]:
        """덤블도어가 제안할 모델들을 훈련시키는 메소드"""

    @abstractmethod
    def predict_survival(self, profile: dict[str, Any]) -> dict[str, Any]:
        """학습된 모델 중 검증 정확도가 가장 높은 모델로 챔피언 프로필의 생존 여부를 예측"""
