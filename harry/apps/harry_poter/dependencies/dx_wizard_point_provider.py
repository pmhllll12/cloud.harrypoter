from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from harry_poter.adapter.outbound.repositories.dx_wizard_point_repository import WizardPointRepository
from harry_poter.app.ports.input.dx_wizard_point_use_case import WizardPointUseCase
from harry_poter.app.ports.output.dx_wizard_point_port import WizardPointPort
from harry_poter.app.use_cases.dx_wizard_point_interactor import WizardPointInteractor


def get_wizard_point_repository(
    db: AsyncSession = Depends(get_db),
) -> WizardPointPort:
    return WizardPointRepository(session=db)


def get_wizard_point_use_case(
    repository: WizardPointPort = Depends(get_wizard_point_repository),
) -> WizardPointUseCase:
    return WizardPointInteractor(repository=repository)
