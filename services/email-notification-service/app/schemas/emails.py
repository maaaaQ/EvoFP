from pydantic import BaseModel, Field


# Базовая схема email'a
class Email(BaseModel):
    sender: str = Field(title="Отправитель")
    receivers: list[str] = Field(title="Получатели")
    subject: str = Field(title="Тема")
    message: str = Field(title="Сообщение")

    class Config:
        orm = True


# Схема по созданию email'a
class EmailCreate(Email):
    id: int = Field(title="Идентификатор email'a")
