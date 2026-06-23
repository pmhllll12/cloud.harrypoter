from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from harry_poter.adapter.outbound.repositories.ax_hogwarts_hertage_repository import HogwartsHeritageRepository
from harry_poter.app.ports.input.ax_hogwarts_hertage_use_case import HogwartsHeritageUseCase
from harry_poter.app.ports.output.ax_hogwarts_hertage_port import HogwartsHeritagePort
from harry_poter.app.use_cases.ax_hogwarts_hertage_interactor import HogwartsHeritageInteractor


def get_hogwarts_heritage_repository(
    db: AsyncSession = Depends(get_db),
) -> HogwartsHeritagePort:
    return HogwartsHeritageRepository(session=db)


def get_hogwarts_heritage_use_case(
    repository: HogwartsHeritagePort = Depends(get_hogwarts_heritage_repository),
) -> HogwartsHeritageUseCase:
    return HogwartsHeritageInteractor(repository=repository)
