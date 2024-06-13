from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(255), nullable=False, unique=True)
    chat_id = Column(Integer, nullable=False, unique=True)
    tg_username = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
