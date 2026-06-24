from __future__ import annotations

from pathlib import Path

from harry_poter.adapter.inbound.api.schemas.ax_hogwarts_hertage_schemas import HogwartsHeritageSchema
from harry_poter.app.dtos.ax_hogwarts_hertage_dto import HogwartsHeritageQuery, HogwartsHeritageResponse
from harry_poter.app.ports.input.ax_hogwarts_hertage_use_case import HogwartsHeritageUseCase
from harry_poter.app.ports.output.ax_hogwarts_hertage_port import HogwartsHeritagePort

_STATIC_DIR = Path(__file__).parents[4] / "core" / "static"


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

    def get_map_page(self, page: str = "index") -> Path:
        '''문묘/성균관 VR 맵 HTML 파일 경로를 반환하는 메소드'''
        html_path = _STATIC_DIR / f"{page}.html"
        if not html_path.exists():
            raise FileNotFoundError(f"{page}.html 파일을 찾을 수 없습니다.")
        return html_path
    