"""성균관 문묘 퀴즈 시드 스크립트.

`python seed_heritage_quiz.py` 를 `harry/` 디렉터리에서 실행하면
heritage_quizzes 테이블에 성균관 문묘 퀴즈 3개를 채운다(이미 있는 항목은 건너뜀).
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

HERITAGE_NAME = "성균관 문묘"

QUIZ_SEED = [
    {
        "question": "성균관 문묘의 대성전에서 제사를 지내는 주요 유교 성인은 누구인가요?",
        "answer": "공자",
        "choices": ["공자", "맹자", "주자", "세종대왕"],
    },
    {
        "question": "성균관 문묘에서 매년 봄·가을에 열리는 전통 제례 행사의 이름은 무엇인가요?",
        "answer": "석전대제",
        "choices": ["석전대제", "종묘제례", "사직대제", "팔관회"],
    },
    {
        "question": "성균관 문묘가 위치한 서울의 행정구역은 어디인가요?",
        "answer": "종로구",
        "choices": ["종로구", "중구", "성북구", "마포구"],
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
