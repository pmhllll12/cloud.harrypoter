from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SexType(str, Enum):
    MALE = "male"
    FEMALE = "female"


@dataclass(frozen=True)
class Sex:
    value: SexType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Sex":
        if raw is None or raw.strip() == "":
            raise ValueError("Sex는 필수 값입니다.")
        try:
            return cls(value=SexType(raw.strip().lower()))
        except ValueError:
            raise ValueError(f"Sex 유효하지 않은 값: '{raw}'")

    @property
    def is_male(self) -> bool:
        return self.value == SexType.MALE

    def __str__(self) -> str:
        return self.value.value
