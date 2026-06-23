from __future__ import annotations

import logging

from harry_poter.app.dtos.sm_weasley_booking_dto import (
    ChampionCommand,
    EntryCommand,
    WeasleyBookingQuery,
    WeasleyBookingResponse,
)
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class WeasleyBookingPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: WeasleyBookingQuery) -> WeasleyBookingResponse:
        raise NotImplementedError

    @abstractmethod
    async def upload_champion_file(self, schema: list) -> WeasleyBookingResponse:
        raise NotImplementedError

    @abstractmethod
    async def receive_uploaded_records(
        self,
        champion_commands: list[ChampionCommand],
        entry_commands: list[EntryCommand],
    ) -> int:
        raise NotImplementedError
