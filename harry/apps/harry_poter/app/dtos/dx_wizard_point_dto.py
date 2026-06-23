from dataclasses import dataclass


@dataclass(frozen=True)
class WizardPointQuery:

    id: int
    name: str


@dataclass(frozen=True)
class WizardPointResponse:

    id: int
    name: str


@dataclass(frozen=True)
class UserPointQuery:

    user_id: int
    amount: int


@dataclass(frozen=True)
class UserPointResponse:

    user_id: int
    total_points: int
