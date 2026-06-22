from dataclasses import dataclass


@dataclass
class ChampionCommand:
    champion_id: str
    name: str
    gender: str
    age: str
    allies_count: str
    mentors_count: str
    survived: str


@dataclass
class EntryCommand:
    school: str
    wand_permit: str
    galleons: str
    tower: str
    wand_core: str


@dataclass
class WeasleyBookingQuery:
    id: int
    name: str


@dataclass
class WeasleyBookingResponse:
    id: int
    name: str
