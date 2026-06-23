from __future__ import annotations

from abc import ABC, abstractmethod

from harry_poter.adapter.inbound.api.schemas.ax_lovegood_course_schemas import LovegoodCourseSchema
from harry_poter.app.dtos.ax_lovegood_course_dto import LovegoodCourseResponse


class LovegoodCourseUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: LovegoodCourseSchema) -> LovegoodCourseResponse:
        raise NotImplementedError
