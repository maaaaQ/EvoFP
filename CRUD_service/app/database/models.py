from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


# Таблица Задач
class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(datetime, default=datetime.utcnow, index=True, nullable=False)
    updated_at = Column(datetime, default=datetime.utcnow, index=True, nullable=False)


# Таблица Категорий
class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    created_at = Column(datetime, default=datetime.utcnow, index=True, nullable=False)
    updated_at = Column(datetime, default=datetime.utcnow, index=True, nullable=False)


# СВязь между таблицами задач и категорий
class task_category(Base):
    __tablename__ = "task_categories"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
