from __future__ import annotations

from abc import ABC, abstractmethod

from harry_poter.app.dtos.ticket_booking_dto import BookingCommand, BookingResponse, UseTicketResponse


class TicketBookingUseCase(ABC):
    @abstractmethod
    async def book_ticket(self, command: BookingCommand) -> BookingResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_ticket(self, ticket_id: str) -> BookingResponse:
        raise NotImplementedError

    @abstractmethod
    async def list_my_tickets(self, user_id: int) -> list[BookingResponse]:
        raise NotImplementedError

    @abstractmethod
    async def use_ticket(self, ticket_id: str) -> UseTicketResponse:
        raise NotImplementedError
