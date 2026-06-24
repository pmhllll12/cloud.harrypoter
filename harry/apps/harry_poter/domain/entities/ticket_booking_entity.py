from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TicketBookingEntity:
    """`TicketBookingOrm`(ticket_bookings) 행과 1:1 대응 — 문화행사 예매 1건."""

    ticket_id: str
    user_id: int
    event_id: int
    booking_status: str
    qr_token: str
    point_used: int
    created_at: datetime
    used_at: datetime | None = None
