from __future__ import annotations

from abc import ABC, abstractmethod

from harry_poter.adapter.inbound.api.schemas.sm_weasley_booking_schemas import WeasleyBookingSchema
from harry_poter.app.dtos.sm_weasley_booking_dto import WeasleyBookingResponse


class WeasleyBookingUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: WeasleyBookingSchema) -> WeasleyBookingResponse:
        raise NotImplementedError

    @abstractmethod
    async def upload_champion_file(self, schema: list[WeasleyBookingSchema]) -> WeasleyBookingResponse:
        raise NotImplementedError
