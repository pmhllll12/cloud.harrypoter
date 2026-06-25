from fastapi import APIRouter, Depends, HTTPException

from harry_poter.adapter.inbound.api.schemas.ticket_booking_schemas import BookingRequestSchema
from harry_poter.app.dtos.ticket_booking_dto import BookingCommand, BookingResponse, UseTicketResponse
from harry_poter.app.ports.input.ticket_booking_use_case import TicketBookingUseCase
from harry_poter.dependencies.ticket_booking_provider import get_ticket_booking_use_case

'''
TICKET_BOOKING (1단계 MVP)
블록체인 없이 "포인트로 예매 -> QR 발급 -> 현장 사용" 흐름만 검증하는 데모 라우터.
회원/포인트/행사 시스템이 아직 없어서 user_id는 그대로 받고, 행사 정보는
domain/constants/dummy_culture_events.py 의 더미 데이터를 사용한다.
'''
ticket_booking_router = APIRouter(prefix="/tickets", tags=["tickets"])


@ticket_booking_router.post("/book", response_model=BookingResponse, summary="문화행사 티켓 예매(포인트 차감)")
async def book_ticket(
    schema: BookingRequestSchema,
    booking: TicketBookingUseCase = Depends(get_ticket_booking_use_case),
) -> BookingResponse:
    try:
        return await booking.book_ticket(BookingCommand(user_id=schema.user_id, event_id=schema.event_id))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@ticket_booking_router.get("/users/{user_id}", response_model=list[BookingResponse], summary="내 예매 티켓 목록")
async def list_my_tickets(
    user_id: int,
    booking: TicketBookingUseCase = Depends(get_ticket_booking_use_case),
) -> list[BookingResponse]:
    return await booking.list_my_tickets(user_id)


@ticket_booking_router.get("/{ticket_id}", response_model=BookingResponse, summary="티켓 상세 조회")
async def get_ticket(
    ticket_id: str,
    booking: TicketBookingUseCase = Depends(get_ticket_booking_use_case),
) -> BookingResponse:
    try:
        return await booking.get_ticket(ticket_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@ticket_booking_router.post("/{ticket_id}/use", response_model=UseTicketResponse, summary="현장 QR 검증 후 입장 처리")
async def use_ticket(
    ticket_id: str,
    booking: TicketBookingUseCase = Depends(get_ticket_booking_use_case),
) -> UseTicketResponse:
    try:
        return await booking.use_ticket(ticket_id)
    except ValueError as exc:
        status_code = 404 if "찾을 수 없습니다" in str(exc) else 409
        raise HTTPException(status_code=status_code, detail=str(exc)) from exc
