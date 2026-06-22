"""데모용 챔피언 명단 시드 스크립트.

`python seed_demo_data.py` 를 `harry/` 디렉터리에서 실행하면 champions·tournament_entries
테이블에 12명의 데모 챔피언을 채운다(이미 있는 champion_id는 건너뛴다).
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parent
_APPS_ROOT = _BACKEND_ROOT / "apps"
_CORE_ROOT = _BACKEND_ROOT / "core"
for _p in (_BACKEND_ROOT, _APPS_ROOT, _CORE_ROOT):
    _p_str = str(_p)
    if _p_str not in sys.path:
        sys.path.append(_p_str)

from sqlalchemy import select

from database import AsyncSessionLocal, create_all_tables, dispose_engine
from harry_poter.adapter.outbound.orm.po_harry_user_orm import HarryUserOrm
from harry_poter.adapter.outbound.orm.sm_dumbledore_store_orm import DumbledoreStoreOrm

# champion_id, name, gender, age, allies_count, mentors_count, survived,
# school(1=Hogwarts/2=Beauxbatons/3=Durmstrang), wand_permit, galleons, tower, wand_core(P/D/U)
DEMO_CHAMPIONS = [
    ("CH001", "Harry Potter", "male", "14", "1", "0", "1", "1", "HP-HOLLY-11", "0", "Gryffindor", "P"),
    ("CH002", "Cedric Diggory", "male", "17", "0", "0", "0", "1", "CD-ASH-12", "5", "Hufflepuff", "D"),
    ("CH003", "Fleur Delacour", "female", "17", "0", "0", "1", "2", "FD-ROSEWOOD-9", "20", "Beauxbatons-Carriage", "U"),
    ("CH004", "Viktor Krum", "male", "18", "0", "1", "1", "3", "VK-HORNBEAM-10", "15", "Durmstrang-Ship", "D"),
    ("CH005", "Hermione Granger", "female", "14", "0", "0", "1", "1", "HG-VINE-10.75", "2", "Gryffindor", "P"),
    ("CH006", "Ron Weasley", "male", "14", "5", "0", "1", "1", "RW-ASH-14", "1", "Gryffindor", "U"),
    ("CH007", "Draco Malfoy", "male", "14", "0", "2", "0", "1", "DM-HAWTHORN-10", "50", "Slytherin", "D"),
    ("CH008", "Cho Chang", "female", "15", "1", "0", "1", "1", "CC-CHERRY-9.5", "8", "Ravenclaw", "P"),
    ("CH009", "Gabrielle Delacour", "female", "8", "1", "1", "1", "2", "GD-WILLOW-8", "25", "Beauxbatons-Carriage", "U"),
    ("CH010", "Neville Longbottom", "male", "14", "0", "2", "0", "1", "NL-CHERRY-13", "3", "Gryffindor", "D"),
    ("CH011", "Luna Lovegood", "female", "13", "0", "0", "1", "1", "LL-DRIFTWOOD-10", "4", "Ravenclaw", "U"),
    ("CH012", "Vincent Crabbe", "male", "14", "1", "0", "0", "1", "VC-UNKNOWN", "10", "Slytherin", "D"),
]


async def main() -> None:
    await create_all_tables()
    async with AsyncSessionLocal() as session:
        inserted = 0
        for champion_id, name, gender, age, allies, mentors, survived, school, wand_permit, galleons, tower, wand_core in DEMO_CHAMPIONS:
            existing = await session.scalar(
                select(HarryUserOrm).where(HarryUserOrm.champion_id == champion_id)
            )
            if existing:
                continue

            session.add(HarryUserOrm(
                champion_id=champion_id,
                name=name,
                gender=gender,
                age=age,
                allies_count=allies,
                mentors_count=mentors,
                survived=survived,
            ))
            session.add(DumbledoreStoreOrm(
                champion_id=champion_id,
                school=school,
                wand_permit=wand_permit,
                galleons=galleons,
                tower=tower,
                wand_core=wand_core,
            ))
            inserted += 1

        await session.commit()
        print(f"챔피언 {inserted}명 신규 삽입 (총 {len(DEMO_CHAMPIONS)}명 중)")
    await dispose_engine()


if __name__ == "__main__":
    asyncio.run(main())
