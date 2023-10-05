import datetime
from uuid import UUID
from app.enums import FilterPriority, FilterCompleted
from pydantic import BaseModel, Field


# Базовая схема задачи
class TasksBase(BaseModel):
    title: str = Field(title="Задача")
    description: str = Field(title="Описание")
    priority: FilterPriority = Field(
        title="Приоритет задачи", default=FilterPriority.low
    )
    is_completed: FilterCompleted = Field(
        title="Статус задачи", default=FilterCompleted.not_completed
    )
    created_at: datetime.datetime = Field(title="Дата создания")
    updated_at: datetime.datetime = Field(title="Дата обновления")
    user_id: UUID = Field(title="Идентификатор пользователя")

    class Config:
        orm = True


# Схема для определения задачи по ее ID
class Tasks(TasksBase):
    id: int = Field(title="Идентификатор задачи", default=None)


# Схема для добавления/обновления задач
class TasksOn(TasksBase):
    pass
