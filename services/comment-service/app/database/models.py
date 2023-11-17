from datetime import datetime
from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP
import uuid
from sqlalchemy.dialects.postgresql import UUID


# Таблица комментариев к задачам
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now, index=True, nullable=False)
    task_id = Column(Integer, index=True, nullable=False, default=1)
