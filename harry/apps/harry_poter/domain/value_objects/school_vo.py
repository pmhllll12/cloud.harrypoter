from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SchoolType(int, Enum):
    """Pclass(1/2/3 등급) 대응 — 트라이위저드 시합에 참가한 3개 마법학교."""

    HOGWARTS = 1
    BEAUXBATONS = 2
    DURMSTRANG = 3


@dataclass(frozen=True)
class School:
    value: SchoolType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "School":
        if raw is None or raw.strip() == "":
            raise ValueError("School은 필수 값입니다.")
        try:
            return cls(value=SchoolType(int(raw.strip())))
        except (ValueError, KeyError):
            raise ValueError(f"School 유효하지 않은 값: '{raw}'")

    @property
    def is_hogwarts(self) -> bool:
        return self.value == SchoolType.HOGWARTS

    def __str__(self) -> str:
        return str(self.value.value)
