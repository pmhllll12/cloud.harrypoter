from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from harry_poter.adapter.inbound.api.schemas.dx_wizard_point_schemas import WizardPointSchema
from harry_poter.app.dtos.dx_wizard_point_dto import WizardPointResponse
from harry_poter.app.ports.input.ax_hogwarts_hertage_use_case import HogwartsHeritageUseCase
from harry_poter.app.ports.input.dx_wizard_point_use_case import WizardPointUseCase
from harry_poter.dependencies.ax_hogwarts_hertage_provider import get_hogwarts_heritage_use_case
from harry_poter.dependencies.dx_wizard_point_provider import get_wizard_point_use_case

'''
위저드 포인트 집계소 (Wizard Point Counter)
호그와트 대형 모래시계처럼 각 피처와 생존(Survived)의 상관관계를 점수로 매겨
순위를 보여주는 역할. 배경 집계·시각화에 어울린다.
'''

wizard_point_router = APIRouter(prefix="/wizardpoint", tags=["wizardpoint"])


@wizard_point_router.get("/myself")
async def introduce_myself(
    wizard_point: WizardPointUseCase = Depends(get_wizard_point_use_case)
) -> WizardPointResponse:
    return await wizard_point.introduce_myself(
        WizardPointSchema(
            id=3,
            name="위저드 포인트 집계소 (Wizard Point Counter)"
        )
    )


@wizard_point_router.get("/correlation-plot")
async def get_correlation_plot(
    wizard_point: WizardPointUseCase = Depends(get_wizard_point_use_case),
    hogwarts: HogwartsHeritageUseCase = Depends(get_hogwarts_heritage_use_case),
) -> StreamingResponse:
    train_set = await hogwarts.get_train_set()
    image_buffer = wizard_point.generate_correlation_plot(train_set)
    return StreamingResponse(image_buffer, media_type="image/png")
