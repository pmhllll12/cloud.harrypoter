from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DummyCultureEvent:
    """행사 마스터 데이터 — 실제 서비스에서는 CULTURE_EVENT 테이블에서 조회한다.

    1단계 MVP 데모이므로 DB 테이블 없이 코드 상수로 둔다.
    """

    event_id: int
    title: str
    ticket_price: int
    total_stock: int


DUMMY_CULTURE_EVENTS: dict[int, DummyCultureEvent] = {
    1001: DummyCultureEvent(event_id=1001, title="경복궁 야간 특별관람", ticket_price=15000, total_stock=50),
    1002: DummyCultureEvent(event_id=1002, title="종묘 제례악 공연", ticket_price=10000, total_stock=30),
    1003: DummyCultureEvent(event_id=1003, title="창덕궁 달빛기행", ticket_price=20000, total_stock=20),
}

DEFAULT_USER_POINT_BALANCE = 50_000
