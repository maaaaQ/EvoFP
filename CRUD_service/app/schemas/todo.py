import datetime
from typing import Optional
from pydantic import BaseModel, Field


# Базвоая схема задачи
class TasksBase(BaseModel):
    title: str = Field(title="Задача")
    description: str = Field(title="Описание")
    category: str = Field(title="Категория задачи")
    is_completed: Optional[bool] = Field(title="Статус задачи")
    created_at: datetime.datetime = Field(title="Дата создания")
    updated_at: datetime.datetime = Field(title="Дата обновления")

    class Config:
        orm = True


# Схема для определния задачи по ее ID
class Tasks(TasksBase):
    id: int = Field(title="Идентификатор задачи", default=None)


# Схема для добавления/обновления задач
class TasksOn(TasksBase):
    pass
