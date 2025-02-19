from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Message(Base):
    """
    Модель сообщения, которая хранится в базе данных.

    Атрибуты:
    - id: Идентификатор сообщения.
    - chat_id: Идентификатор чата, к которому относится сообщение.
    - user_id: Идентификатор пользователя, отправившего сообщение.
    - message: Текст сообщения.
    - message_date: Дата и время отправки сообщения.
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    message_date = Column(DateTime, default=datetime.utcnow)

