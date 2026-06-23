from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from matrix.grid_neo_theone_base import Base


class WizardPointOrm(Base):

    __abstract__ = True


class UserPointOrm(Base):
    __tablename__ = "user_points"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
