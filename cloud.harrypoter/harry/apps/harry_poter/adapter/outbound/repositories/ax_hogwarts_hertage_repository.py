import logging

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from harry_poter.adapter.outbound.orm.po_harry_user_orm import HarryUserOrm
from harry_poter.adapter.outbound.orm.sm_dumbledore_store_orm import DumbledoreStoreOrm
from harry_poter.app.dtos.ax_hogwarts_hertage_dto import HogwartsHeritageQuery, HogwartsHeritageResponse
from harry_poter.app.ports.output.ax_hogwarts_hertage_port import HogwartsHeritagePort

logger = logging.getLogger(__name__)


def _to_row(c: HarryUserOrm, e: DumbledoreStoreOrm | None, include_survived: bool) -> dict:
    row = {
        "ChampionId":    c.champion_id,
        "Name":          c.name,
        "gender":        c.gender,  # 인터렉터가 소문자 gender 기대
        "Age":           c.age,
        "AlliesCount":   c.allies_count,
        "MentorsCount":  c.mentors_count,
        "School":        e.school       if e else None,
        "WandPermit":    e.wand_permit  if e else None,
        "Galleons":      e.galleons     if e else None,
        "Tower":         e.tower        if e else None,
        "WandCore":      e.wand_core    if e else None,
    }
    if include_survived:
        row["Survived"] = c.survived
    return row


class HogwartsHeritageRepository(HogwartsHeritagePort):
    """PostgreSQL을 이용한 호그와트 헤리티지의 챔피언 명단 관리 저장소."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_train_set(self) -> pd.DataFrame:
        ''' Survived 컬럼이 있는 데이터 전체를 데이터 프레임으로 반환하는 메소드 '''
        stmt = (
            select(HarryUserOrm, DumbledoreStoreOrm)
            .outerjoin(DumbledoreStoreOrm, DumbledoreStoreOrm.champion_id == HarryUserOrm.champion_id)
            .where(HarryUserOrm.survived.isnot(None))
        )
        result = await self.session.execute(stmt)
        rows = [_to_row(c, e, include_survived=True) for c, e in result.all()]
        logger.info("[HogwartsHeritageRepository] get_train_set rows=%d", len(rows))
        return pd.DataFrame(rows)

    async def get_test_set(self) -> pd.DataFrame:
        ''' Survived 컬럼이 없는 데이터 전체를 데이터 프레임으로 반환하는 메소드 '''
        stmt = (
            select(HarryUserOrm, DumbledoreStoreOrm)
            .outerjoin(DumbledoreStoreOrm, DumbledoreStoreOrm.champion_id == HarryUserOrm.champion_id)
            .where(HarryUserOrm.survived.is_(None))
        )
        result = await self.session.execute(stmt)
        rows = [_to_row(c, e, include_survived=False) for c, e in result.all()]
        logger.info("[HogwartsHeritageRepository] get_test_set rows=%d", len(rows))
        return pd.DataFrame(rows)

    def introduce_myself(self, query: HogwartsHeritageQuery) -> HogwartsHeritageResponse:
        logger.info("[HogwartsHeritageRepository] introduce_myself id=%s name=%s", query.id, query.name)
        return HogwartsHeritageResponse(
            id=query.id,
            name=query.name,
            memo=query.memo,
        )
