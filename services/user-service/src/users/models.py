from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, relationship

from src.users import database


class Group(database.BASE):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String)


class User(SQLAlchemyBaseUserTableUUID, database.BASE):
    first_name = Column(String(length=128), nullable=True)
    last_name = Column(String(length=128), nullable=True)
    nickname = Column(String(length=64), nullable=True)
    age = Column(Integer(), nullable=True)
    group_id = mapped_column(ForeignKey("group.id"))
    group = relationship("Group", uselist=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with database.initializer.async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
