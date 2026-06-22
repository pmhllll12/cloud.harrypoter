from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from harry_poter.adapter.outbound.repositories.sm_weasley_booking_repository import WeasleyBookingRepository
from harry_poter.app.ports.input.sm_weasley_booking_use_case import WeasleyBookingUseCase
from harry_poter.app.ports.output.sm_weasley_booking_port import WeasleyBookingPort
from harry_poter.app.use_cases.sm_weasley_booking_interactor import WeasleyBookingInteractor


def get_weasley_booking_repository(
    db: AsyncSession = Depends(get_db),
) -> WeasleyBookingPort:
    return WeasleyBookingRepository(session=db)


def get_weasley_booking_use_case(
    repository: WeasleyBookingPort = Depends(get_weasley_booking_repository),
) -> WeasleyBookingUseCase:
    return WeasleyBookingInteractor(repository=repository)
