from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from harry_poter.adapter.inbound.api.schemas.ax_hogwarts_hertage_schemas import HogwartsHeritageSchema
from harry_poter.app.dtos.ax_hogwarts_hertage_dto import HogwartsHeritageResponse


class HogwartsHeritageUseCase(ABC):

    @abstractmethod
    async def get_train_set(self) -> pd.DataFrame:
        '''호그와트 헤리티지가 DB에서 훈련 데이터셋(생존 결과가 있는 챔피언)을 가져오는 메소드'''
        pass

    @abstractmethod
    async def get_test_set(self) -> pd.DataFrame:
        '''호그와트 헤리티지가 DB에서 테스트 데이터셋(생존 결과가 없는 챔피언)을 가져오는 메소드'''
        pass

    @abstractmethod
    def introduce_myself(self, schema: HogwartsHeritageSchema) -> HogwartsHeritageResponse:
        '''호그와트 헤리티지의 자기소개 메소드'''
        pass
