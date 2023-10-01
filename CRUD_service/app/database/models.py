from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from datetime import datetime

from .database import Base


# Таблица Задач
class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False, default="Important")
    is_completed = Column(Boolean, default=False, index=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now, index=True, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.now, index=True, nullable=False)
