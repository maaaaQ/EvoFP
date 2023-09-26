import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DATETIME
from sqlalchemy.orm import relationship

from .database import Base


class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DATETIME, default=datetime.utcnow, index=True, nullable=False)
    updated_at = Column(DATETIME, default=datetime.utcnow, index=True, nullable=False)


class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    created_at = Column(DATETIME, default=datetime.utcnow, index=True, nullable=False)
    updated_at = Column(DATETIME, default=datetime.utcnow, index=True, nullable=False)


class task_category(Base):
    __tablename__ = "task_categories"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
