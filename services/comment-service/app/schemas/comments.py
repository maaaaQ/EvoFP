import datetime
from uuid import UUID
from pydantic import BaseModel, Field


# Базовая схема комментариев
class CommentsBase(BaseModel):
    text: str = Field(title="Текст комментария")
    user_id: UUID = Field(title="Идентификатор пользователя оставившего комментарий")
    created_at: datetime.datetime = Field(title="Дата создания комментария")

    class Config:
        orm = True


# Схема по созданию комментария
class CommentsCreate(CommentsBase):
    task_id: int = Field(title="Идентификатор задачи")


# Схема по обновлению комментария
class CommentsUpdate(CommentsBase):
    task_id: int = Field(title="Идентификатор задачи")


# Схема по определению комментария по ID
class Comments(CommentsBase):
    id: int = Field(title="Идентификатор комментария")
    task_id: int = Field(title="Идентификатор задачи")
