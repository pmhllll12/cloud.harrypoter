from __future__ import annotations

from harry_poter.adapter.inbound.api.schemas.ax_hogwarts_hertage_schemas import HogwartsHeritageSchema
from harry_poter.app.dtos.ax_hogwarts_hertage_dto import HogwartsHeritageQuery, HogwartsHeritageResponse
from harry_poter.app.ports.input.ax_hogwarts_hertage_use_case import HogwartsHeritageUseCase
from harry_poter.app.ports.output.ax_hogwarts_hertage_port import HogwartsHeritagePort


class HogwartsHeritageInteractor(HogwartsHeritageUseCase):
    def __init__(self, repository: HogwartsHeritagePort) -> None:
        self.repository = repository

    async def get_train_set(self) -> "pd.DataFrame":
        '''호그와트 헤리티지가 DB에서 train set(생존 결과가 있는 챔피언)만 가져오는 메소드'''
        return await self.repository.get_train_set()

    async def get_test_set(self) -> "pd.DataFrame":
        '''호그와트 헤리티지가 DB에서 test set(생존 결과가 없는 챔피언)만 가져오는 메소드'''
        return await self.repository.get_test_set()

    def introduce_myself(self, schema: HogwartsHeritageSchema) -> HogwartsHeritageResponse:
        query = HogwartsHeritageQuery(id=schema.id, name=schema.name, memo=schema.memo)
        return self.repository.introduce_myself(query)
