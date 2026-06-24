from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from harry_poter.adapter.outbound.repositories.dx_sphinx_quiz_repository import SphinxQuizRepository
from harry_poter.app.ports.input.dx_sphinx_quiz_use_case import SphinxQuizUseCase
from harry_poter.app.ports.input.dx_wizard_point_use_case import WizardPointUseCase
from harry_poter.app.ports.input.po_harry_user_use_case import HarryUserUseCase
from harry_poter.app.ports.output.dx_sphinx_quiz_port import SphinxQuizPort
from harry_poter.app.use_cases.dx_sphinx_quiz_interactor import SphinxQuizInteractor
from harry_poter.dependencies.dx_wizard_point_provider import get_wizard_point_use_case
from harry_poter.dependencies.po_harry_user_provider import get_harry_user_use_case


def get_sphinx_quiz_repository(
    db: AsyncSession = Depends(get_db),
) -> SphinxQuizPort:
    return SphinxQuizRepository(session=db)


def get_sphinx_quiz_use_case(
    repository: SphinxQuizPort = Depends(get_sphinx_quiz_repository),
    harry: HarryUserUseCase = Depends(get_harry_user_use_case),
    wizard_point: WizardPointUseCase = Depends(get_wizard_point_use_case),
) -> SphinxQuizUseCase:
    return SphinxQuizInteractor(repository=repository, harry=harry, wizard_point=wizard_point)
