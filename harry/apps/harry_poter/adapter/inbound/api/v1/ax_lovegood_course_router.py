from fastapi import APIRouter, Depends

from harry_poter.adapter.inbound.api.schemas.ax_lovegood_course_schemas import LovegoodCourseSchema
from harry_poter.app.dtos.ax_lovegood_course_dto import LovegoodCourseResponse
from harry_poter.app.ports.input.ax_lovegood_course_use_case import LovegoodCourseUseCase
from harry_poter.dependencies.ax_lovegood_course_provider import get_lovegood_course_use_case

'''
루나 러브굿 (Luna Lovegood)
남들이 보지 못하는 것을 보는 독특한 시야로 숨겨진 패턴을 잘 찾아냅니다.
원본 데이터를 모델이 먹을 수 있는 피처로 가공하는 코스(여정) 설계 역할.
'''

lovegood_course_router = APIRouter(prefix="/lovegood", tags=["lovegood"])


@lovegood_course_router.get("/myself")
async def introduce_myself(
    lovegood: LovegoodCourseUseCase = Depends(get_lovegood_course_use_case)
) -> LovegoodCourseResponse:
    return await lovegood.introduce_myself(
        LovegoodCourseSchema(
            id=8,
            name="루나 러브굿 (Luna Lovegood)"
        )
    )
