from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class WandCoreType(str, Enum):
    """Embarked(승선항) 대응 — 챔피언 지팡이의 심재(코어) 종류."""

    PHOENIX_FEATHER = "P"
    DRAGON_HEARTSTRING = "D"
    UNICORN_HAIR = "U"


@dataclass(frozen=True)
class WandCore:
    value: WandCoreType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "WandCore":
        if raw is None or raw.strip() == "":
            raise ValueError("WandCore는 필수 값입니다.")
        try:
            return cls(value=WandCoreType(raw.strip().upper()))
        except ValueError:
            raise ValueError(f"WandCore 유효하지 않은 값: '{raw}'")

    def __str__(self) -> str:
        return self.value.value
