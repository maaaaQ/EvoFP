import datetime
from pydantic import BaseModel, Field


class TasksBase(BaseModel):
    title: str = Field(title="Задача")
    description: str = Field(title="Описание")
    is_completed: Optional[bool] = Field(title="Статус задачи")
    created_at: datetime = Field(title="Дата создания")
    updated_at: datetime = Field(title="Дата обновления")

    class Config:
        orm = True


class CategoryBase(BaseModel):
    name: str = Field(title="Категория")
    created_at: datetime = Field(title="Дата создания")
    updated_at: datetime = Field(title="Дата обновления")

    class Config:
        orm = True
