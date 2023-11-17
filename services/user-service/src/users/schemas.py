import uuid

from fastapi_users import schemas
from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
    group_id: int = 2

    class Config:
        orm_mode = True


class GroupRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class GroupUpsert(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class GroupUpdate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserRead(schemas.BaseUser[uuid.UUID]):
    first_name: str | None = None
    last_name: str | None = None
    nickname: str | None = None
    age: int | None = None
    group_id: int | None = None


class UserCreate(schemas.BaseUserCreate):
    first_name: str = None
    last_name: str = None
    nickname: str = None
    age: int = None
    group_id: int | None = None


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str = None
    last_name: str = None
    nickname: str = None
    age: int = None
    group_id: int | None = None
