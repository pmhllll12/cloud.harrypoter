from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from harry_poter.adapter.outbound.repositories.po_harry_user_repository import HarryUserRepository
from harry_poter.app.ports.input.po_harry_user_use_case import HarryUserUseCase
from harry_poter.app.ports.output.po_harry_user_port import HarryUserPort
from harry_poter.app.use_cases.po_harry_user_interactor import HarryUserInteractor


def get_harry_user_repository(
    db: AsyncSession = Depends(get_db),
) -> HarryUserPort:
    return HarryUserRepository(session=db)


def get_harry_user_use_case(
    repository: HarryUserPort = Depends(get_harry_user_repository),
) -> HarryUserUseCase:
    return HarryUserInteractor(repository=repository)
