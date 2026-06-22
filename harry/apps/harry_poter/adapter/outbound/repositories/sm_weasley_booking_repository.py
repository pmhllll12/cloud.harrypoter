from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from harry_poter.adapter.inbound.api.schemas.sm_weasley_booking_schemas import WeasleyBookingSchema
from harry_poter.app.dtos.sm_weasley_booking_dto import (
    ChampionCommand,
    EntryCommand,
    WeasleyBookingQuery,
    WeasleyBookingResponse,
)
from harry_poter.app.ports.output.sm_weasley_booking_port import WeasleyBookingPort

logger = logging.getLogger(__name__)


class WeasleyBookingRepository(WeasleyBookingPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: WeasleyBookingQuery) -> WeasleyBookingResponse:
        logger.info("[WeasleyBookingRepository] introduce_myself | request_data=%s", query)
        return WeasleyBookingResponse(id=query.id, name=query.name)

    async def upload_champion_file(self, schema: list[WeasleyBookingSchema]) -> WeasleyBookingResponse:
        # PostgreSQL·SQLite 둘 다에서 동작하도록 dialect 전용 upsert(`ON CONFLICT`) 대신
        # select 후 있으면 갱신, 없으면 추가하는 방식으로 처리한다.
        from sqlalchemy import select
        from harry_poter.adapter.outbound.orm.po_harry_user_orm import HarryUserOrm
        from harry_poter.adapter.outbound.orm.sm_dumbledore_store_orm import DumbledoreStoreOrm

        valid_rows = [r for r in schema if r.champion_id]
        if not valid_rows:
            return WeasleyBookingResponse(id=0, name="저장할 유효 행이 없습니다.")

        saved = 0
        for r in valid_rows:
            champion = await self.session.scalar(
                select(HarryUserOrm).where(HarryUserOrm.champion_id == r.champion_id)
            )
            survived = r.survived if r.survived not in (None, "") else None
            if champion:
                champion.name = r.name or ""
                champion.gender = r.gender or ""
                champion.age = r.age or ""
                champion.allies_count = r.allies_count or "0"
                champion.mentors_count = r.mentors_count or "0"
                champion.survived = survived
            else:
                self.session.add(HarryUserOrm(
                    champion_id=r.champion_id,
                    name=r.name or "",
                    gender=r.gender or "",
                    age=r.age or "",
                    allies_count=r.allies_count or "0",
                    mentors_count=r.mentors_count or "0",
                    survived=survived,
                ))

            entry = await self.session.scalar(
                select(DumbledoreStoreOrm).where(DumbledoreStoreOrm.champion_id == r.champion_id)
            )
            if entry:
                entry.school = r.school or ""
                entry.wand_permit = r.wand_permit or ""
                entry.galleons = r.galleons or ""
                entry.tower = r.tower or ""
                entry.wand_core = r.wand_core or ""
            else:
                self.session.add(DumbledoreStoreOrm(
                    champion_id=r.champion_id,
                    school=r.school or "",
                    wand_permit=r.wand_permit or "",
                    galleons=r.galleons or "",
                    tower=r.tower or "",
                    wand_core=r.wand_core or "",
                ))
            saved += 1

        await self.session.commit()
        logger.info("[WeasleyBookingRepository] upload_champion_file saved=%d", saved)
        return WeasleyBookingResponse(id=saved, name=f"CSV {saved}행 저장 완료")

    async def receive_uploaded_records(
        self,
        champion_commands: list[ChampionCommand],
        entry_commands: list[EntryCommand],
    ) -> int:
        from harry_poter.adapter.outbound.orm.po_harry_user_orm import HarryUserOrm
        from harry_poter.adapter.outbound.orm.sm_dumbledore_store_orm import DumbledoreStoreOrm

        champion_orms = [
            HarryUserOrm(
                champion_id=cmd.champion_id,
                name=cmd.name,
                gender=cmd.gender,
                age=cmd.age,
                allies_count=cmd.allies_count,
                mentors_count=cmd.mentors_count,
                survived=cmd.survived,
            )
            for cmd in champion_commands
        ]
        self.session.add_all(champion_orms)
        await self.session.flush()

        entry_orms = [
            DumbledoreStoreOrm(
                champion_id=champion_orm.champion_id,
                school=cmd.school,
                wand_permit=cmd.wand_permit,
                galleons=cmd.galleons,
                tower=cmd.tower,
                wand_core=cmd.wand_core,
            )
            for champion_orm, cmd in zip(champion_orms, entry_commands)
        ]
        self.session.add_all(entry_orms)
        await self.session.commit()

        return len(champion_orms)
