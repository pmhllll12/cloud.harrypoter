from __future__ import annotations

from harry_poter.adapter.outbound.orm.dx_sphinx_quiz_orm import HeritageQuizOrm
from harry_poter.app.dtos.dx_sphinx_quiz_dto import HeritageQuizItem


def heritage_quiz_item_from_orm(orm: HeritageQuizOrm) -> HeritageQuizItem:
    return HeritageQuizItem(
        id=orm.id,
        heritage_name=orm.heritage_name,
        question=orm.question,
        answer=orm.answer,
        choices=tuple(orm.choices),
    )


__all__ = ["heritage_quiz_item_from_orm"]
