from fastapi import APIRouter, Depends
from harry_poter.adapter.inbound.api.schemas.po_harry_user_schemas import HarryUserSchema
from harry_poter.app.dtos.po_harry_user_dto import HarryUserResponse
from harry_poter.app.ports.input.po_harry_user_use_case import HarryUserUseCase
from harry_poter.dependencies.po_harry_user_provider import get_harry_user_use_case

'''
해리 포터 (Harry Potter)
주인공 
(반강제로) 트라이위저드 시합에 참가한 4번째 챔피언. 생존 예측 모델의
핵심 학습·예측 인터페이스를 담당합니다.
'''

harry_user_router = APIRouter(prefix="/harry", tags=["harry"])


@harry_user_router.get("/myself")
async def introduce_myself(
    harry: HarryUserUseCase = Depends(get_harry_user_use_case)
) -> HarryUserResponse:
    return await harry.introduce_myself(
        HarryUserSchema(
            id=4,
            name="해리 포터 (Harry Potter)"
        )
    )
