from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from harry_poter.domain.entities.ticket_booking_entity import TicketBookingEntity


class TicketBookingPort(ABC):
    """티켓 예매 영속화 — DB(ORM)와의 경계."""

    @abstractmethod
    async def save_ticket(
        self,
        ticket_id: str,
        user_id: int,
        event_id: int,
        qr_token: str,
        point_used: int,
        created_at: datetime,
    ) -> TicketBookingEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_ticket(self, ticket_id: str) -> TicketBookingEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def list_tickets_by_user(self, user_id: int) -> list[TicketBookingEntity]:
        raise NotImplementedError

    @abstractmethod
    async def mark_used(self, ticket_id: str, used_at: datetime) -> TicketBookingEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_user_point_balance(self, user_id: int) -> int:
        """더미 유저 포인트 잔액 조회 — 처음 보는 user_id는 기본 잔액으로 자동 시드."""
        raise NotImplementedError

    @abstractmethod
    async def deduct_point(self, user_id: int, amount: int) -> int:
        """포인트 차감 후 남은 잔액을 반환."""
        raise NotImplementedError

    @abstractmethod
    async def count_all_tickets(self) -> int:
        """ticket_id 순번(TICKET-2026-000001) 생성에 쓰는 발급 누적 건수."""
        raise NotImplementedError
