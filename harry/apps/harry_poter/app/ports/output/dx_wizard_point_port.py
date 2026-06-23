from __future__ import annotations

from abc import ABC, abstractmethod

from harry_poter.app.dtos.dx_wizard_point_dto import UserPointQuery, UserPointResponse, WizardPointQuery, WizardPointResponse


class WizardPointPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: WizardPointQuery) -> WizardPointResponse:
        raise NotImplementedError

    @abstractmethod
    async def save_point(self, query: UserPointQuery) -> UserPointResponse:
        raise NotImplementedError
