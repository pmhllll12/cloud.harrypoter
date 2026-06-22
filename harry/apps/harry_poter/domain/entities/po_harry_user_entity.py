from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HarryUserEntity:
    """해리(유저) 챔피언 행 — `HarryUserOrm`(champions 테이블) 컬럼과 1:1 대응."""

    id: int | None
    champion_id: str | None
    name: str | None
    gender: str | None
    age: str | None
    allies_count: str | None
    mentors_count: str | None
    survived: str | None
