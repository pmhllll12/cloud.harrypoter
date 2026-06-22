from fastapi import APIRouter, Depends

from harry_poter.adapter.inbound.api.schemas.sm_dumbledore_store_schemas import DumbledoreStoreSchema
from harry_poter.app.dtos.sm_dumbledore_store_dto import DumbledoreStoreResponse
from harry_poter.app.ports.input.sm_dumbledore_store_use_case import DumbledoreStoreUseCase
from harry_poter.dependencies.sm_dumbledore_store_provider import get_dumbledore_store_use_case

'''
알버스 덤블도어 (Albus Dumbledore)
트라이위저드 시합의 최종 책임자이자, 여러 예측 알고리즘(전략)을 한 곳에
모아두는 지혜의 저장소(Strategy Registry) 역할.
'''

dumbledore_store_router = APIRouter(prefix="/dumbledore", tags=["dumbledore"])


@dumbledore_store_router.get("/myself")
async def introduce_myself(
    dumbledore: DumbledoreStoreUseCase = Depends(get_dumbledore_store_use_case)
) -> DumbledoreStoreResponse:
    return await dumbledore.introduce_myself(
        DumbledoreStoreSchema(
            id=0,
            name="알버스 덤블도어 (Albus Dumbledore)"
        )
    )
