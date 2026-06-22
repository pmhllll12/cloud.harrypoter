from __future__ import annotations

from harry_poter.adapter.inbound.api.schemas.sm_weasley_booking_schemas import WeasleyBookingSchema
from harry_poter.app.dtos.sm_weasley_booking_dto import WeasleyBookingQuery, WeasleyBookingResponse
from harry_poter.app.ports.input.sm_weasley_booking_use_case import WeasleyBookingUseCase
from harry_poter.app.ports.output.sm_weasley_booking_port import WeasleyBookingPort


class WeasleyBookingInteractor(WeasleyBookingUseCase):
    def __init__(self, repository: WeasleyBookingPort) -> None:
        self.repository = repository

    async def introduce_myself(self, schema: WeasleyBookingSchema) -> WeasleyBookingResponse:
        query = WeasleyBookingQuery(
            id=schema.id if schema.id is not None else 0,
            name=schema.name or "",
        )
        return await self.repository.introduce_myself(query)

    async def upload_champion_file(self, schema: list[WeasleyBookingSchema]) -> WeasleyBookingResponse:
        return await self.repository.upload_champion_file(schema)
