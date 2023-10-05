import uuid
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from .database import Base


# Таблица Задач
class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=False)
    priority = Column(Integer, index=True, nullable=False, default="0")
    is_completed = Column(Boolean, default=False, index=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now, index=True, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.now, index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, nullable=False)
