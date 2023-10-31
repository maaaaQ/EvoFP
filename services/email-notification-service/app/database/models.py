from .database import Base
from sqlalchemy import Column, Integer, String


# Таблица электронных писем
class EventNotification(Base):
    __tablename__ = "event_notifications"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True, nullable=False)
    receivers = Column(String, index=True, nullable=False)
    subject = Column(String, max_length=100, index=True, nullable=False)
    message = Column(String, max_length=1000, index=True, nullable=False)
