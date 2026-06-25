"""보은 법주사 퀴즈 시드 스크립트.

`python seed_beopjusa_quiz.py` 를 `harry/` 디렉터리에서 실행하면
heritage_quizzes 테이블에 보은 법주사 퀴즈 3개를 채운다(이미 있는 항목은 건너뜀).
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
from harry_poter.adapter.outbound.orm.dx_sphinx_quiz_orm import HeritageQuizOrm

HERITAGE_NAME = "보은 법주사"

QUIZ_SEED = [
    {
        "question": "법주사가 위치한 국립공원의 이름은?",
        "answer": "속리산",
        "choices": ["지리산", "설악산", "속리산", "덕유산"],
    },
    {
        "question": "법주사에 있는 우리나라에서 유일하게 현존하는 목조 5층 불탑의 이름은?",
        "answer": "팔상전",
        "choices": ["다보탑", "팔상전", "석가탑", "원각사지탑"],
    },
    {
        "question": "법주사를 창건한 승려는 누구인가요?",
        "answer": "의신대사",
        "choices": ["의상대사", "의신대사", "의천대사", "서산대사"],
    },
]


async def main() -> None:
    await create_all_tables()
    async with AsyncSessionLocal() as session:
        inserted = 0
        for item in QUIZ_SEED:
            existing = await session.scalar(
                select(HeritageQuizOrm).where(
                    HeritageQuizOrm.heritage_name == HERITAGE_NAME,
                    HeritageQuizOrm.question == item["question"],
                )
            )
            if existing:
                continue

            session.add(HeritageQuizOrm(
                heritage_name=HERITAGE_NAME,
                question=item["question"],
                answer=item["answer"],
                choices=item["choices"],
            ))
            inserted += 1

        await session.commit()
        print(f"퀴즈 {inserted}개 신규 삽입 (총 {len(QUIZ_SEED)}개 중)")
    await dispose_engine()


if __name__ == "__main__":
    asyncio.run(main())
