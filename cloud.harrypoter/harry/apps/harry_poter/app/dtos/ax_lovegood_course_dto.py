from dataclasses import dataclass


@dataclass(frozen=True)
class LovegoodCourseQuery:
    id: int
    name: str


@dataclass(frozen=True)
class LovegoodCourseResponse:
    id: int
    name: str
