from __future__ import annotations

from harry_poter.adapter.outbound.orm.sm_dumbledore_store_orm import DumbledoreStoreOrm
from harry_poter.domain.entities.sm_dumbledore_store_entity import DumbledoreStoreEntity


def dumbledore_store_entity_from_orm(orm: DumbledoreStoreOrm) -> DumbledoreStoreEntity:
    return DumbledoreStoreEntity(
        id=orm.id,
        champion_id=orm.champion_id,
        school=orm.school,
        wand_permit=orm.wand_permit,
        galleons=orm.galleons,
        tower=orm.tower,
        wand_core=orm.wand_core,
    )


def dumbledore_store_orm_from_entity(entity: DumbledoreStoreEntity) -> DumbledoreStoreOrm:
    kw: dict = {
        "champion_id": entity.champion_id,
        "school": entity.school,
        "wand_permit": entity.wand_permit,
        "galleons": entity.galleons,
        "tower": entity.tower,
        "wand_core": entity.wand_core,
    }
    if entity.id is not None:
        kw["id"] = entity.id
    return DumbledoreStoreOrm(**kw)


__all__ = ["dumbledore_store_entity_from_orm", "dumbledore_store_orm_from_entity"]
