from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class BookingCommand:
    """예매 요청 — 사용자가 어떤 행사를 예매할지."""

    user_id: int
    event_id: int


@dataclass
class BookingResponse:
    """예매 결과 — 발급된 티켓 정보."""

    ticket_id: str
    user_id: int
    event_id: int
    event_title: str
    booking_status: str
    qr_token: str
    point_used: int
    created_at: datetime
    used_at: datetime | None


@dataclass
class UseTicketResponse:
    """현장 입장 처리(QR 검증) 결과."""

    ticket_id: str
    booking_status: str
    used_at: datetime | None
    message: str
