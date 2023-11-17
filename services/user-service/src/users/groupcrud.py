import typing

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.users import models, schemas


# Создает новую группу пользователей
async def create_group(
    group: schemas.GroupCreate, session: AsyncSession
) -> models.Group:
    db_group = models.Group(name=group.name)

    session.add(db_group)
    await session.commit()
    await session.refresh(db_group)
    return db_group


# Возвращает информацию о всех группах пользователей
async def get_all_groups(
    session: AsyncSession, skip: int = 0, limit: int = 100
) -> typing.List[models.Group]:
    result = await session.execute(select(models.Group).offset(skip).limit(limit))
    return result.scalars().all()


# Возвращает информацию о конкретной группе пользователей по ID
async def get_group_by_id(session: AsyncSession, group_id: int) -> models.Group:
    result = await session.execute(
        select(models.Group).filter(models.Group.id == group_id).limit(1)
    )
    return result.scalars().one_or_none()


# Обновляет группу пользователей
async def update_group(
    session: AsyncSession, group_id: int, group: schemas.GroupUpdate
) -> models.Group:
    result = await session.execute(
        update(models.Group)
        .where(models.Group.id == group_id)
        .values(group.model_dump())
    )
    await session.commit()
    if result:
        return await get_group_by_id(session, group_id)
    return None


async def upsert_group(
    session: AsyncSession, group: schemas.GroupUpsert
) -> models.Group:
    stm = insert(models.Group).values(group.model_dump())
    stm = stm.on_conflict_do_update(constraint="group_pkey", set_={"name": group.name})
    result = await session.execute(stm)

    await session.commit()
    if result:
        return await get_group_by_id(session, group.id)
    return None


#  Удаляет информацию  о группе пользователей
async def delete_group(session: AsyncSession, group_id: int) -> bool:
    has_group = await get_group_by_id(session, group_id)
    await session.execute(delete(models.Group).filter(models.Group.id == group_id))
    await session.commit()
    return bool(has_group)
