from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from harry_poter.adapter.outbound.repositories.po_professor_festival_repository import ProfessorFestivalRepository
from harry_poter.app.ports.input.ax_hermione_route_use_case import HermioneRouteUseCase
from harry_poter.app.ports.input.ax_hogwarts_hertage_use_case import HogwartsHeritageUseCase
from harry_poter.app.ports.input.ax_lovegood_course_use_case import LovegoodCourseUseCase
from harry_poter.app.ports.input.dx_sphinx_quiz_use_case import SphinxQuizUseCase
from harry_poter.app.ports.input.dx_wizard_point_use_case import WizardPointUseCase
from harry_poter.app.ports.input.po_harry_user_use_case import HarryUserUseCase
from harry_poter.app.ports.input.po_professor_festival_use_case import ProfessorFestivalUseCase
from harry_poter.app.ports.input.sm_dumbledore_store_use_case import DumbledoreStoreUseCase
from harry_poter.app.ports.output.po_professor_festival_port import ProfessorFestivalPort
from harry_poter.app.use_cases.po_professor_festival_interactor import ProfessorFestivalInteractor
from harry_poter.dependencies.ax_hermione_route_provider import get_hermione_route_use_case
from harry_poter.dependencies.ax_hogwarts_hertage_provider import get_hogwarts_heritage_use_case
from harry_poter.dependencies.ax_lovegood_course_provider import get_lovegood_course_use_case
from harry_poter.dependencies.dx_sphinx_quiz_provider import get_sphinx_quiz_use_case
from harry_poter.dependencies.dx_wizard_point_provider import get_wizard_point_use_case
from harry_poter.dependencies.po_harry_user_provider import get_harry_user_use_case
from harry_poter.dependencies.sm_dumbledore_store_provider import get_dumbledore_store_use_case


def get_professor_festival_repository(
    db: AsyncSession = Depends(get_db),
) -> ProfessorFestivalPort:
    return ProfessorFestivalRepository(session=db)


def get_professor_festival_use_case(
    repository: ProfessorFestivalPort = Depends(get_professor_festival_repository),
    hermione: HermioneRouteUseCase    = Depends(get_hermione_route_use_case),
    harry: HarryUserUseCase           = Depends(get_harry_user_use_case),
    dumbledore: DumbledoreStoreUseCase = Depends(get_dumbledore_store_use_case),
    sphinx: SphinxQuizUseCase         = Depends(get_sphinx_quiz_use_case),
    hogwarts: HogwartsHeritageUseCase = Depends(get_hogwarts_heritage_use_case),
    lovegood: LovegoodCourseUseCase   = Depends(get_lovegood_course_use_case),
    wizard_point: WizardPointUseCase  = Depends(get_wizard_point_use_case),
) -> ProfessorFestivalUseCase:

    return ProfessorFestivalInteractor(
        repository=repository,
        hermione=hermione,
        harry=harry,
        dumbledore=dumbledore,
        sphinx=sphinx,
        hogwarts=hogwarts,
        lovegood=lovegood,
        wizard_point=wizard_point,
    )
