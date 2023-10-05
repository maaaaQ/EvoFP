import uuid
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, Enum
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
from app.enums import FilterPriority, FilterCompleted


# Таблица Задач
class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=False)
    priority = Column(
        Enum(FilterPriority), index=True, nullable=False, default=FilterPriority.low
    )
    is_completed = Column(
        Enum(FilterCompleted),
        index=True,
        nullable=False,
        default=FilterCompleted.not_completed,
    )
    created_at = Column(TIMESTAMP, default=datetime.now, index=True, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.now, index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, nullable=False)
