from __future__ import annotations

import logging
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from harry_poter.adapter.outbound.orm.ticket_booking_orm import DummyUserPointOrm, TicketBookingOrm
from harry_poter.app.ports.output.ticket_booking_port import TicketBookingPort
from harry_poter.domain.constants.dummy_culture_events import DEFAULT_USER_POINT_BALANCE
from harry_poter.domain.entities.ticket_booking_entity import TicketBookingEntity

logger = logging.getLogger(__name__)

_BOOKING_STATUS_BOOKED = "BOOKED"


class TicketBookingRepository(TicketBookingPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_ticket(
        self,
        ticket_id: str,
        user_id: int,
        event_id: int,
        qr_token: str,
        point_used: int,
        created_at: datetime,
    ) -> TicketBookingEntity:
        orm = TicketBookingOrm(
            ticket_id=ticket_id,
            user_id=user_id,
            event_id=event_id,
            booking_status=_BOOKING_STATUS_BOOKED,
            qr_token=qr_token,
            point_used=point_used,
            created_at=created_at,
        )
        self.session.add(orm)
        await self.session.commit()
        return self._to_entity(orm)

    async def get_ticket(self, ticket_id: str) -> TicketBookingEntity | None:
        orm = await self.session.scalar(
            select(TicketBookingOrm).where(TicketBookingOrm.ticket_id == ticket_id)
        )
        return self._to_entity(orm) if orm else None

    async def list_tickets_by_user(self, user_id: int) -> list[TicketBookingEntity]:
        orms = await self.session.scalars(
            select(TicketBookingOrm)
            .where(TicketBookingOrm.user_id == user_id)
            .order_by(TicketBookingOrm.created_at.desc())
        )
        return [self._to_entity(orm) for orm in orms]

    async def mark_used(self, ticket_id: str, used_at: datetime) -> TicketBookingEntity:
        orm = await self.session.scalar(
            select(TicketBookingOrm).where(TicketBookingOrm.ticket_id == ticket_id)
        )
        if orm is None:
            raise ValueError(f"티켓을 찾을 수 없습니다 (ticket_id={ticket_id}).")
        orm.booking_status = "USED"
        orm.used_at = used_at
        await self.session.commit()
        return self._to_entity(orm)

    async def get_user_point_balance(self, user_id: int) -> int:
        orm = await self.session.scalar(
            select(DummyUserPointOrm).where(DummyUserPointOrm.user_id == user_id)
        )
        if orm is None:
            orm = DummyUserPointOrm(user_id=user_id, point_balance=DEFAULT_USER_POINT_BALANCE)
            self.session.add(orm)
            await self.session.commit()
            logger.info("[TicketBookingRepository] seeded dummy user_id=%s balance=%s", user_id, orm.point_balance)
        return orm.point_balance

    async def deduct_point(self, user_id: int, amount: int) -> int:
        orm = await self.session.scalar(
            select(DummyUserPointOrm).where(DummyUserPointOrm.user_id == user_id)
        )
        if orm is None:
            orm = DummyUserPointOrm(user_id=user_id, point_balance=DEFAULT_USER_POINT_BALANCE)
            self.session.add(orm)
        orm.point_balance -= amount
        await self.session.commit()
        return orm.point_balance

    async def count_all_tickets(self) -> int:
        result = await self.session.scalar(select(func.count()).select_from(TicketBookingOrm))
        return result or 0

    def _to_entity(self, orm: TicketBookingOrm) -> TicketBookingEntity:
        return TicketBookingEntity(
            ticket_id=orm.ticket_id,
            user_id=orm.user_id,
            event_id=orm.event_id,
            booking_status=orm.booking_status,
            qr_token=orm.qr_token,
            point_used=orm.point_used,
            created_at=orm.created_at,
            used_at=orm.used_at,
        )
