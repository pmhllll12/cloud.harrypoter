from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from matrix.grid_neo_theone_base import Base


class DumbledoreStoreOrm(Base):
    # 위즐리 업로드용 ORM과 테이블명 충돌 방지
    __tablename__ = "tournament_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    champion_id: Mapped[str | None] = mapped_column(String, ForeignKey("champions.champion_id"), nullable=True)
    school: Mapped[str | None] = mapped_column(String, nullable=True)
    wand_permit: Mapped[str | None] = mapped_column(String, nullable=True)
    galleons: Mapped[str | None] = mapped_column(String, nullable=True)
    tower: Mapped[str | None] = mapped_column(String, nullable=True)
    wand_core: Mapped[str | None] = mapped_column(String, nullable=True)
