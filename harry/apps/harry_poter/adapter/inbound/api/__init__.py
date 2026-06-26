"""HTTP API adapters — Harry Poter v1 라우터를 한 데 묶어 노출."""

from __future__ import annotations

from fastapi import APIRouter

from harry_poter.adapter.inbound.api.v1.ax_hermione_route_router import hermione_route_router
from harry_poter.adapter.inbound.api.v1.ax_hogwarts_hertage_router import hogwarts_hertage_router
from harry_poter.adapter.inbound.api.v1.ax_lovegood_course_router import lovegood_course_router
from harry_poter.adapter.inbound.api.v1.dx_sphinx_quiz_router import sphinx_quiz_router
from harry_poter.adapter.inbound.api.v1.dx_wizard_point_router import wizard_point_router
from harry_poter.adapter.inbound.api.v1.po_harry_user_router import harry_user_router
from harry_poter.adapter.inbound.api.v1.po_professor_festival_router import professor_festival_router
from harry_poter.adapter.inbound.api.v1.sm_dumbledore_store_router import dumbledore_store_router
from harry_poter.adapter.inbound.api.v1.sm_weasley_booking_router import weasley_booking_router
from harry_poter.adapter.inbound.api.v1.ticket_booking_router import ticket_booking_router
from harry_poter.adapter.inbound.api.v1.tourism_chat_router import tourism_chat_router

harry_poter_router = APIRouter(prefix="/harry-poter", tags=["harry-poter"])


@harry_poter_router.get("/", summary="Harry Poter API 안내")
async def harry_poter_root() -> dict[str, str]:
    """`/harry-poter` 아래 캐릭터별 엔드포인트 목록(상위에 `/harry-poter` 한 번만 붙습니다)."""
    return {
        "message": "Harry Poter demo API",
        "paths": {
            "hermione_myself": "/harry-poter/hermione/myself",
            "hogwarts_myself": "/harry-poter/hogwarts/myself",
            "lovegood_myself": "/harry-poter/lovegood/myself",
            "sphinx_myself": "/harry-poter/sphinx/myself",
            "wizardpoint_myself": "/harry-poter/wizardpoint/myself",
            "wizardpoint_correlation_plot": "/harry-poter/wizardpoint/correlation-plot",
            "harry_myself": "/harry-poter/harry/myself",
            "dumbledore_myself": "/harry-poter/dumbledore/myself",
            "weasley_myself": "/harry-poter/weasley/myself",
            "weasley_upload": "/harry-poter/weasley/upload",
            "professor_myself": "/harry-poter/professor/myself",
            "professor_chat": "/harry-poter/professor/chat",
            "ticket_book": "/harry-poter/tickets/book",
            "ticket_my_list": "/harry-poter/tickets/users/{user_id}",
            "ticket_detail": "/harry-poter/tickets/{ticket_id}",
            "ticket_use": "/harry-poter/tickets/{ticket_id}/use",
        },
    }


harry_poter_router.include_router(weasley_booking_router)
harry_poter_router.include_router(ticket_booking_router)
harry_poter_router.include_router(dumbledore_store_router)
harry_poter_router.include_router(hogwarts_hertage_router)
harry_poter_router.include_router(hermione_route_router)
harry_poter_router.include_router(sphinx_quiz_router)
harry_poter_router.include_router(wizard_point_router)
harry_poter_router.include_router(lovegood_course_router)
harry_poter_router.include_router(harry_user_router)
harry_poter_router.include_router(professor_festival_router)
harry_poter_router.include_router(tourism_chat_router)

__all__ = ["harry_poter_router"]
