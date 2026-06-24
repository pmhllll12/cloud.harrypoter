from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from matrix.grid_neo_theone_base import Base


class HeritageQuizOrm(Base):
    __tablename__ = "heritage_quizzes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    heritage_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    question: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str] = mapped_column(String, nullable=False)
    choices: Mapped[list] = mapped_column(JSON, nullable=False, default=list)


class UserQuizProgressOrm(Base):
    __tablename__ = "user_quiz_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    quiz_id: Mapped[int] = mapped_column(Integer, ForeignKey("heritage_quizzes.id"), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
