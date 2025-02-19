from datetime import datetime
from typing import List

from pydantic import BaseModel
from pydantic import Field


class SendMessageSchema(BaseModel):
    """
    Схема для отправки сообщения.

    Атрибуты:
    - chat_id: ID чата, должно быть больше 0.
    - user_id: ID пользователя, должно быть больше 0.
    - message: Текст сообщения, длина от 1 до 500 символов.
    """
    chat_id: int = Field(..., gt=0, description="ID чата должен быть больше 0")
    user_id: int = Field(..., gt=0, description="ID пользователя должен быть больше 0")
    message: str = Field(..., min_length=1, max_length=500, description="Сообщение должно содержать от 1 до 500 символов")


class MessageResponseSchema(BaseModel):
    """
    Схема для ответа с сообщением.

    Атрибуты:
    - chat_id: ID чата.
    - user_id: ID пользователя.
    - message: Текст сообщения.
    - message_date: Дата и время отправки сообщения.
    """
    chat_id: int
    user_id: int
    message: str
    message_date: datetime

    class Config:
        """ Конфигурация для работы с аттрибутами моделей."""
        from_attributes = True


class MessageListResponse(BaseModel):
    """
    Схема для списка сообщений.
    Атрибуты:
    - messages: Список объектов MessageResponseSchema.
    """
    messages: List[MessageResponseSchema]
