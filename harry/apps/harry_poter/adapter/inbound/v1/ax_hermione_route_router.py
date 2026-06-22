from fastapi import APIRouter, Depends

from harry_poter.adapter.inbound.api.schemas.ax_hermione_route_schemas import HermioneRouteSchema
from harry_poter.app.dtos.ax_hermione_route_dto import HermioneRouteResponse
from harry_poter.app.ports.input.ax_hermione_route_use_case import HermioneRouteUseCase
from harry_poter.dependencies.ax_hermione_route_provider import get_hermione_route_use_case

'''
헤르미온느 그레인저 (Hermione Granger)
도서관을 통째로 외운 듣한 지식과 빠른 판단력으로 위기마다 해결책을 찾아내는 인물.
질문 의도를 분류하고 라우팅하는 NLU 두뇌 역할을 담당합니다.
'''

hermione_route_router = APIRouter(prefix="/hermione", tags=["hermione"])


@hermione_route_router.get("/myself")
async def introduce_myself(
    hermione: HermioneRouteUseCase = Depends(get_hermione_route_use_case)
) -> HermioneRouteResponse:
    return await hermione.introduce_myself(
        HermioneRouteSchema(
            id=1,
            name="헤르미온느 그레인저 (Hermione Granger)"
        )
    )
