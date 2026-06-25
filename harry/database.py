"""SQLite 비동기 연결 — 로컬 데모용.

`titanic`(minho)은 Neon/PostgreSQL을 쓰지만, harry_poter는 별도 DB 서버 없이
바로 띄워볼 수 있도록 로컬 SQLite 파일을 기본값으로 둔다. 운영 DB가 생기면
`DATABASE_URL` 환경변수만 PostgreSQL 비동기 URL로 바꾸면 된다.
"""

from __future__ import annotations

import logging
import os
from collections.abc import AsyncGenerator
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()

logger = logging.getLogger(__name__)

_DB_PATH = Path(__file__).resolve().parent / "harry_poter.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{_DB_PATH}")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Depends — 요청마다 세션을 열고 닫습니다."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            if session.in_transaction():
                await session.rollback()
            raise


async def create_all_tables() -> None:
    """champions·tournament_entries 테이블이 없으면 생성합니다."""
    from matrix.grid_neo_theone_base import Base
    from harry_poter.adapter.outbound.orm import po_harry_user_orm  # noqa: F401
    from harry_poter.adapter.outbound.orm import sm_dumbledore_store_orm  # noqa: F401
    from harry_poter.adapter.outbound.orm import ticket_booking_orm  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("DB create_all 완료 (champions, tournament_entries, ticket_bookings, dummy_user_points)")


async def dispose_engine() -> None:
    """앱 종료 시 연결 풀 정리."""
    await engine.dispose()
