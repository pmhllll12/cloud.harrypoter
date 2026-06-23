from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

_MIN_GALLEONS = 0.0


@dataclass(frozen=True)
class Galleons:
    """Fare(탑승 요금) 대응 — 챔피언이 시합에 등록할 때 낸 갈레온(마법사 화폐) 보증금."""

    value: Optional[float]

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Galleons":
        if raw is None or raw.strip() == "":
            return cls(value=None)
        try:
            value = float(raw.strip())
        except ValueError:
            raise ValueError(f"Galleons는 숫자여야 합니다: '{raw}'")
        if value < _MIN_GALLEONS:
            raise ValueError(f"Galleons는 {_MIN_GALLEONS} 이상이어야 합니다: {value}")
        return cls(value=value)

    def per_ally(self, ally_count: int) -> Optional[float]:
        if self.value is None or ally_count <= 0:
            return None
        return self.value / ally_count

    def __str__(self) -> str:
        return str(self.value) if self.value is not None else "Unknown"
