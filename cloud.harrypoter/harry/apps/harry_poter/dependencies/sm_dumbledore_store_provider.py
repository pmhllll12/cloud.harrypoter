from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from harry_poter.adapter.outbound.repositories.sm_dumbledore_store_repository import DumbledoreStoreRepository
from harry_poter.app.ports.input.sm_dumbledore_store_use_case import DumbledoreStoreUseCase
from harry_poter.app.ports.output.sm_dumbledore_store_port import DumbledoreStorePort
from harry_poter.app.use_cases.sm_dumbledore_store_interactor import DumbledoreStoreInteractor


def get_dumbledore_store_repository(
    db: AsyncSession = Depends(get_db),
) -> DumbledoreStorePort:
    return DumbledoreStoreRepository(session=db)


def get_dumbledore_store_use_case(
    repository: DumbledoreStorePort = Depends(get_dumbledore_store_repository),
) -> DumbledoreStoreUseCase:
    return DumbledoreStoreInteractor(repository=repository)
