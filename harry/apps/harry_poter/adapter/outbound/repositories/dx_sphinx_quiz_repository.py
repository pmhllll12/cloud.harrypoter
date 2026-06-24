from __future__ import annotations

import logging

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from harry_poter.adapter.outbound.mapper.dx_sphinx_quiz_mapper import heritage_quiz_item_from_orm
from harry_poter.adapter.outbound.orm.dx_sphinx_quiz_orm import HeritageQuizOrm, UserQuizProgressOrm
from harry_poter.app.dtos.dx_sphinx_quiz_dto import HeritageQuizItem, SphinxQuizQuery, SphinxQuizResponse
from harry_poter.app.ports.output.dx_sphinx_quiz_port import SphinxQuizPort

logger = logging.getLogger(__name__)


class SphinxQuizRepository(SphinxQuizPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: SphinxQuizQuery) -> SphinxQuizResponse:
        logger.info("[SphinxQuizRepository] introduce_myself | request_data=%s", query)
        return SphinxQuizResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )

    async def search_heritage(self, keyword: str) -> SphinxQuizResponse:
        stmt = (
            select(HeritageQuizOrm)
            .where(HeritageQuizOrm.heritage_name.ilike(f"%{keyword}%"))
            .limit(1)
        )
        result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()
        if orm is None:
            return SphinxQuizResponse(id=0, name=keyword)
        return SphinxQuizResponse(id=orm.id, name=orm.heritage_name)

    async def get_quizzes_by_heritage(self, heritage_name: str) -> list[HeritageQuizItem]:
        stmt = select(HeritageQuizOrm).where(HeritageQuizOrm.heritage_name == heritage_name)
        result = await self.session.execute(stmt)
        orms = result.scalars().all()
        logger.info("[SphinxQuizRepository] get_quizzes_by_heritage heritage=%s count=%d", heritage_name, len(orms))
        return [heritage_quiz_item_from_orm(o) for o in orms]

    async def get_quiz_by_id(self, quiz_id: int) -> HeritageQuizItem:
        stmt = select(HeritageQuizOrm).where(HeritageQuizOrm.id == quiz_id)
        result = await self.session.execute(stmt)
        orm = result.scalar_one()
        return heritage_quiz_item_from_orm(orm)

    async def get_user_progress(self, user_id: int, heritage_name: str) -> list[int]:
        stmt = (
            select(UserQuizProgressOrm.quiz_id)
            .join(HeritageQuizOrm, HeritageQuizOrm.id == UserQuizProgressOrm.quiz_id)
            .where(
                and_(
                    UserQuizProgressOrm.user_id == user_id,
                    UserQuizProgressOrm.is_correct.is_(True),
                    HeritageQuizOrm.heritage_name == heritage_name,
                )
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def save_quiz_result(self, user_id: int, quiz_id: int, is_correct: bool) -> None:
        progress = UserQuizProgressOrm(user_id=user_id, quiz_id=quiz_id, is_correct=is_correct)
        self.session.add(progress)
        await self.session.flush()
        logger.info(
            "[SphinxQuizRepository] save_quiz_result user_id=%s quiz_id=%s is_correct=%s",
            user_id, quiz_id, is_correct,
        )
