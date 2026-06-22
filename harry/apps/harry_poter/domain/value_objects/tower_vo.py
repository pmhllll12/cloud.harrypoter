from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Tower:
    """Cabin(객실) 대응 — 챔피언이 머무른 호그와트 기숙사 탑(동)."""

    value: Optional[str]

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Tower":
        if raw is None or raw.strip() == "":
            return cls(value=None)
        return cls(value=raw.strip())

    @property
    def block(self) -> Optional[str]:
        return self.value[0] if self.value else None

    @property
    def has_tower(self) -> bool:
        return self.value is not None

    def __str__(self) -> str:
        return self.value if self.value is not None else "Unknown"
