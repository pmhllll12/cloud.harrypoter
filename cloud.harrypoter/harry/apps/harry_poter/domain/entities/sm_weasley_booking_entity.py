from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WeasleyChampionEntity:
    """위즐리 업로드 `HarryUserOrm`(champions) 행과 1:1 대응."""

    champion_id: str
    name: str
    gender: str
    age: str
    allies_count: str
    mentors_count: str
    survived: str
    id: int | None = None


@dataclass
class WeasleyEntryEntity:
    """위즐리 업로드 `DumbledoreStoreOrm`(tournament_entries) 행과 1:1 대응."""

    champion_id: str | None
    school: str
    wand_permit: str
    galleons: str
    tower: str
    wand_core: str
    id: int | None = None
