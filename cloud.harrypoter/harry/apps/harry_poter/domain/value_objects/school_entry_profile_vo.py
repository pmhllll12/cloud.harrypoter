from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from harry_poter.domain.value_objects.galleons_vo import Galleons
from harry_poter.domain.value_objects.school_vo import School
from harry_poter.domain.value_objects.tower_vo import Tower
from harry_poter.domain.value_objects.wand_core_vo import WandCore


@dataclass(frozen=True)
class SchoolEntryProfile:
    """Survived와 상관관계가 높은 School·Galleons·Tower·WandCore를 묶은 임베디드 값 타입.

    titanic의 TravelClassProfile(Pclass-Fare 상관) 대응 — 학교 등록 정보가
    서로 강하게 얽혀 있어 개별 필드보다 하나의 값 타입으로 묶는다.
    """

    school: School
    galleons: Galleons
    tower: Tower
    wand_core: WandCore

    @classmethod
    def from_raw(
        cls,
        school_raw: Optional[str],
        galleons_raw: Optional[str],
        tower_raw: Optional[str],
        wand_core_raw: Optional[str],
    ) -> "SchoolEntryProfile":
        return cls(
            school=School.from_raw(school_raw),
            galleons=Galleons.from_raw(galleons_raw),
            tower=Tower.from_raw(tower_raw),
            wand_core=WandCore.from_raw(wand_core_raw),
        )

    def __str__(self) -> str:
        return f"{self.school}등급/{self.galleons}/{self.tower}/{self.wand_core}"
