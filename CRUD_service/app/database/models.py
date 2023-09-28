from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
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
    created_at = Column(TIMESTAMP, default=datetime.now, index=True, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.now, index=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Categories", back_populates="tasks")


# Таблица Категорий
class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now, index=True, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.now, index=True, nullable=False)

    tasks = relationship("Tasks", back_populates="category")
