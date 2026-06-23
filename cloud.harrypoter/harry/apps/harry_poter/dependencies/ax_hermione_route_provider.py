from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from harry_poter.adapter.outbound.repositories.ax_hermione_route_repository import HermioneRouteRepository
from harry_poter.app.ports.output.ax_hermione_route_port import HermioneRoutePort
from database import get_db
from harry_poter.app.ports.input.ax_hermione_route_use_case import HermioneRouteUseCase
from harry_poter.app.use_cases.ax_hermione_route_interactor import HermioneRouteInteractor

def get_hermione_route_repository(
        db : AsyncSession = Depends(get_db)
) -> HermioneRoutePort:

        return HermioneRouteRepository(session=db)

def get_hermione_route_use_case(
        repository : HermioneRoutePort = Depends(get_hermione_route_repository)
) -> HermioneRouteUseCase:

        return HermioneRouteInteractor(repository=repository)
