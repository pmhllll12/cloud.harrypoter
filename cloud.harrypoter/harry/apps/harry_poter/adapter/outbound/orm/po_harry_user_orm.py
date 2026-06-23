from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from matrix.grid_neo_theone_base import Base


class HarryUserOrm(Base):
    # 클래스명은 HarryUserOrm이고, 테이블명은 champions로 지정합니다.
    __tablename__ = "champions"

    champion_id: Mapped[str | None] = mapped_column(String, primary_key=True, nullable=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    gender: Mapped[str | None] = mapped_column(String, nullable=True)
    age: Mapped[str | None] = mapped_column(String, nullable=True)
    allies_count: Mapped[str | None] = mapped_column(String, nullable=True)
    mentors_count: Mapped[str | None] = mapped_column(String, nullable=True)
    survived: Mapped[str | None] = mapped_column(String, nullable=True)
