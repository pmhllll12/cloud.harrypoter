from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)  # 생성 후 수정 불가하도록 설정
class HogwartsHeritageQuery:

    id: int  # 직관적인 타입 변경
    name: str
    memo: Optional[str] = None


@dataclass(frozen=True)  # 생성 후 수정 불가하도록 설정
class HogwartsHeritageResponse:

    id: int  # 직관적인 타입 변경
    name: str
    memo: Optional[str] = None
