from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from harry_poter.adapter.outbound.repositories.ticket_booking_repository import TicketBookingRepository
from harry_poter.app.ports.input.ticket_booking_use_case import TicketBookingUseCase
from harry_poter.app.ports.output.ticket_booking_port import TicketBookingPort
from harry_poter.app.use_cases.ticket_booking_interactor import TicketBookingInteractor


def get_ticket_booking_repository(
    db: AsyncSession = Depends(get_db),
) -> TicketBookingPort:
    return TicketBookingRepository(session=db)


def get_ticket_booking_use_case(
    repository: TicketBookingPort = Depends(get_ticket_booking_repository),
) -> TicketBookingUseCase:
    return TicketBookingInteractor(repository=repository)
