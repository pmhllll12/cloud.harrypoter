from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from harry_poter.adapter.outbound.orm.dx_wizard_point_orm import UserPointOrm
from harry_poter.app.dtos.dx_wizard_point_dto import UserPointQuery, UserPointResponse, WizardPointQuery, WizardPointResponse
from harry_poter.app.ports.output.dx_wizard_point_port import WizardPointPort

logger = logging.getLogger(__name__)


class WizardPointRepository(WizardPointPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: WizardPointQuery) -> WizardPointResponse:
        logger.info("[WizardPointRepository] introduce_myself | request_data=%s", query)
        return WizardPointResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )

    async def save_point(self, query: UserPointQuery) -> UserPointResponse:
        stmt = select(UserPointOrm).where(UserPointOrm.user_id == query.user_id)
        result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()

        if orm is None:
            orm = UserPointOrm(user_id=query.user_id, total_points=query.amount)
            self.session.add(orm)
        else:
            orm.total_points += query.amount

        await self.session.flush()
        logger.info(
            "[WizardPointRepository] save_point user_id=%s earned=%s total=%s",
            orm.user_id, query.amount, orm.total_points,
        )
        return UserPointResponse(user_id=orm.user_id, total_points=orm.total_points)
