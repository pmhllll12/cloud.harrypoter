from fastapi import APIRouter, Depends

from harry_poter.adapter.inbound.api.schemas.ax_hogwarts_hertage_schemas import HogwartsHeritageSchema
from harry_poter.app.dtos.ax_hogwarts_hertage_dto import HogwartsHeritageResponse
from harry_poter.app.ports.input.ax_hogwarts_hertage_use_case import HogwartsHeritageUseCase
from harry_poter.dependencies.ax_hogwarts_hertage_provider import get_hogwarts_heritage_use_case

'''
호그와트 헤리티지 기록보관소 (Hogwarts Heritage Archive)
수백 년간 쌓인 입학·시합 기록을 보관하는 곳. 트라이위저드 시합 챔피언 명단을
train/test 셋으로 보관·제공하는 저장소 역할.
'''

hogwarts_hertage_router = APIRouter(prefix="/hogwarts", tags=["hogwarts"])


@hogwarts_hertage_router.get("/myself")
async def introduce_myself(
    hogwarts: HogwartsHeritageUseCase = Depends(get_hogwarts_heritage_use_case)
) -> HogwartsHeritageResponse:
    return await hogwarts.introduce_myself(
        HogwartsHeritageSchema(
            id=1,
            name="호그와트 헤리티지 기록보관소 (Hogwarts Heritage Archive)"
        )
    )
