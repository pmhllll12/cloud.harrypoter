from __future__ import annotations

from harry_poter.adapter.outbound.orm.po_harry_user_orm import HarryUserOrm
from harry_poter.domain.entities.po_harry_user_entity import HarryUserEntity


def harry_user_entity_from_orm(orm: HarryUserOrm) -> HarryUserEntity:
    return HarryUserEntity(
        id=orm.id,
        champion_id=orm.champion_id,
        name=orm.name,
        gender=orm.gender,
        age=orm.age,
        allies_count=orm.allies_count,
        mentors_count=orm.mentors_count,
        survived=orm.survived,
    )


def harry_user_orm_from_entity(entity: HarryUserEntity) -> HarryUserOrm:
    kw: dict = {
        "champion_id": entity.champion_id,
        "name": entity.name,
        "gender": entity.gender,
        "age": entity.age,
        "allies_count": entity.allies_count,
        "mentors_count": entity.mentors_count,
        "survived": entity.survived,
    }
    if entity.id is not None:
        kw["id"] = entity.id
    return HarryUserOrm(**kw)


__all__ = ["harry_user_entity_from_orm", "harry_user_orm_from_entity"]
