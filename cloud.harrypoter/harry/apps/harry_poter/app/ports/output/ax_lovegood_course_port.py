from __future__ import annotations

from abc import ABC, abstractmethod

from harry_poter.app.dtos.ax_lovegood_course_dto import LovegoodCourseQuery, LovegoodCourseResponse


class LovegoodCoursePort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: LovegoodCourseQuery) -> LovegoodCourseResponse:
        raise NotImplementedError
