import datetime
from typing import Optional
from pydantic import BaseModel, Field


Def = {
    "title": "Задача",
    "description": "Изучение Fast API",
    "is_completed": False,
    "created_at": datetime.datetime.now(),
    "updated_at": datetime.datetime.now(),
}


# Базвоая схема задачи
class TasksBase(BaseModel):
    title: str = Field(title="Задача")
    description: str = Field(title="Описание")
    is_completed: Optional[bool] = Field(title="Статус задачи")
    created_at: datetime.datetime = Field(title="Дата создания")
    updated_at: datetime.datetime = Field(title="Дата обновления")
    about: str = Field(title="Идентификатор задачи", default=Def)

    class Config:
        orm = True


# Схема для определния задачи по ее ID
class Tasks(TasksBase):
    id: int = Field(title="Идентификатор задачи", default=None)


# Схема для добавления/обновления задач
class TasksOn(TasksBase):
    pass


# Базовая схема категорий
class CategoryBase(BaseModel):
    name: str = Field(title="Категория")
    created_at: datetime.datetime = Field(title="Дата создания")
    updated_at: datetime.datetime = Field(title="Дата обновления")

    class Config:
        orm = True
