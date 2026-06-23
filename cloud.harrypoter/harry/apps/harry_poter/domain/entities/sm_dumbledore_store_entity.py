from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DumbledoreStoreEntity:
    """덤블도어(전략 저장소) 시합 등록 행 — `DumbledoreStoreOrm`(tournament_entries) 과 1:1 대응."""

    id: int | None
    champion_id: str | None
    school: str | None
    wand_permit: str | None
    galleons: str | None
    tower: str | None
    wand_core: str | None
