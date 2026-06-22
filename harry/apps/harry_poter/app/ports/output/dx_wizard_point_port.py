from __future__ import annotations

from abc import ABC, abstractmethod

from harry_poter.app.dtos.dx_wizard_point_dto import WizardPointQuery, WizardPointResponse


class WizardPointPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: WizardPointQuery) -> WizardPointResponse:
        raise NotImplementedError
