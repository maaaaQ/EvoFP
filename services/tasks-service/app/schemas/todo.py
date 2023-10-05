import datetime
from uuid import UUID

from pydantic import BaseModel, Field


# Базовая схема задачи
class TasksBase(BaseModel):
    title: str = Field(title="Задача")
    description: str = Field(title="Описание")
    priority: int = Field(
        title="Приоритет задачи",
        description="Выбери приоритет задачи: 0 - низкий, 1 - высокий",
        ge=0,
        le=1,
        default=0,
    )
    is_completed: bool = Field(
        title="Статус задачи",
        description="Выбери статус задачи:true - выполнена, false - в процессе",
        default=False,
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
