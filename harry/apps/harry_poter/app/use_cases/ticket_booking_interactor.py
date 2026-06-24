from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from harry_poter.app.dtos.ticket_booking_dto import BookingCommand, BookingResponse, UseTicketResponse
from harry_poter.app.ports.input.ticket_booking_use_case import TicketBookingUseCase
from harry_poter.app.ports.output.ticket_booking_port import TicketBookingPort
from harry_poter.domain.constants.dummy_culture_events import DUMMY_CULTURE_EVENTS
from harry_poter.domain.entities.ticket_booking_entity import TicketBookingEntity

logger = logging.getLogger(__name__)

BOOKING_STATUS_BOOKED = "BOOKED"
BOOKING_STATUS_USED = "USED"


class TicketBookingInteractor(TicketBookingUseCase):
    """1단계 MVP: 블록체인 없이 '포인트로 예매 -> QR 발급 -> 현장 사용' 흐름만 검증한다.

    행사 마스터 데이터는 DUMMY_CULTURE_EVENTS 상수를 쓰고, 포인트 잔액은
    repository가 user_id별로 더미 시드(기본 잔액)해서 관리한다.
    """

    def __init__(self, repository: TicketBookingPort) -> None:
        self.repository = repository

    async def book_ticket(self, command: BookingCommand) -> BookingResponse:
        event = DUMMY_CULTURE_EVENTS.get(command.event_id)
        if event is None:
            raise ValueError(f"존재하지 않는 행사입니다 (event_id={command.event_id}).")

        balance = await self.repository.get_user_point_balance(command.user_id)
        if balance < event.ticket_price:
            raise ValueError(
                f"포인트가 부족합니다 (보유 {balance}P, 필요 {event.ticket_price}P)."
            )

        await self.repository.deduct_point(command.user_id, event.ticket_price)

        sequence = await self.repository.count_all_tickets() + 1
        ticket_id = f"TICKET-{datetime.now(timezone.utc).year}-{sequence:06d}"
        qr_token = uuid.uuid4().hex

        entity = await self.repository.save_ticket(
            ticket_id=ticket_id,
            user_id=command.user_id,
            event_id=command.event_id,
            qr_token=qr_token,
            point_used=event.ticket_price,
            created_at=datetime.now(timezone.utc),
        )
        logger.info("[TicketBookingInteractor] booked ticket_id=%s user_id=%s", ticket_id, command.user_id)
        return self._to_response(entity)

    async def get_ticket(self, ticket_id: str) -> BookingResponse:
        entity = await self.repository.get_ticket(ticket_id)
        if entity is None:
            raise ValueError(f"티켓을 찾을 수 없습니다 (ticket_id={ticket_id}).")
        return self._to_response(entity)

    async def list_my_tickets(self, user_id: int) -> list[BookingResponse]:
        entities = await self.repository.list_tickets_by_user(user_id)
        return [self._to_response(entity) for entity in entities]

    async def use_ticket(self, ticket_id: str) -> UseTicketResponse:
        entity = await self.repository.get_ticket(ticket_id)
        if entity is None:
            raise ValueError(f"티켓을 찾을 수 없습니다 (ticket_id={ticket_id}).")
        if entity.booking_status == BOOKING_STATUS_USED:
            raise ValueError("이미 사용된 티켓입니다 (중복 입장 차단).")

        updated = await self.repository.mark_used(ticket_id, datetime.now(timezone.utc))
        logger.info("[TicketBookingInteractor] used ticket_id=%s", ticket_id)
        return UseTicketResponse(
            ticket_id=updated.ticket_id,
            booking_status=updated.booking_status,
            used_at=updated.used_at,
            message="입장 처리 완료",
        )

    def _to_response(self, entity: TicketBookingEntity) -> BookingResponse:
        event = DUMMY_CULTURE_EVENTS.get(entity.event_id)
        return BookingResponse(
            ticket_id=entity.ticket_id,
            user_id=entity.user_id,
            event_id=entity.event_id,
            event_title=event.title if event else "알 수 없는 행사",
            booking_status=entity.booking_status,
            qr_token=entity.qr_token,
            point_used=entity.point_used,
            created_at=entity.created_at,
            used_at=entity.used_at,
        )
