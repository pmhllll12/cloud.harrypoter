from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from matrix.grid_neo_theone_base import Base


class TicketBookingOrm(Base):
    """TICKET_BOOKING 테이블 — 1단계 MVP: 블록체인 없이 예매 상태만 보관."""

    __tablename__ = "ticket_bookings"

    ticket_id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False)
    booking_status: Mapped[str] = mapped_column(String, nullable=False)
    qr_token: Mapped[str] = mapped_column(String, nullable=False)
    point_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class DummyUserPointOrm(Base):
    """USER 포인트 잔액 — 실제 회원 시스템이 없는 데모용 더미 테이블.

    처음 보는 user_id는 DEFAULT_USER_POINT_BALANCE로 자동 시드된다.
    """

    __tablename__ = "dummy_user_points"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    point_balance: Mapped[int] = mapped_column(Integer, nullable=False)
