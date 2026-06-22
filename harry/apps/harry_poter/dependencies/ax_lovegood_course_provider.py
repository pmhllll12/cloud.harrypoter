from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from harry_poter.adapter.outbound.repositories.ax_lovegood_course_repository import LovegoodCourseRepository
from harry_poter.app.ports.input.ax_lovegood_course_use_case import LovegoodCourseUseCase
from harry_poter.app.ports.output.ax_lovegood_course_port import LovegoodCoursePort
from harry_poter.app.use_cases.ax_lovegood_course_interactor import LovegoodCourseInteractor


def get_lovegood_course_repository(
    db: AsyncSession = Depends(get_db),
) -> LovegoodCoursePort:
    return LovegoodCourseRepository(session=db)


def get_lovegood_course_use_case(
    repository: LovegoodCoursePort = Depends(get_lovegood_course_repository),
) -> LovegoodCourseUseCase:
    return LovegoodCourseInteractor(repository=repository)
