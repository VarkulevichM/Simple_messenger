from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.core.log_file import logger
from app.schemas.message import MessageListResponse
from app.schemas.message import MessageResponseSchema
from app.services.message_service import MessageService

router = APIRouter()


@router.post("/send_message", response_model=MessageResponseSchema)
async def send_message(chat_id: int, user_id: int, message: str, service: MessageService = Depends()) -> MessageResponseSchema:
    """
    Эндпоинт для отправки сообщения.

    :param chat_id: ID чата.
    :param user_id: ID пользователя.
    :param message: Текст сообщения.
    :param service: Сервис для обработки логики отправки сообщения.
    """
    try:
        return await service.send_message(chat_id, user_id, message)
    except Exception as error:
        logger.error(f"Ошибка ендпойнта send_message: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/messages", response_model=MessageListResponse)
async def get_messages(chat_id: int, limit: int = 10, offset: int = 0, service: MessageService = Depends()) -> MessageListResponse:
    """
    Эндпоинт для получения списка сообщений из чата.

    :param chat_id: ID чата.
    :param limit: Максимальное количество сообщений для получения.
    :param offset: Количество сообщений, которые нужно пропустить.
    :param service: Сервис для получения сообщений.
    """
    try:
        messages = await service.get_messages(chat_id, limit, offset)
        return MessageListResponse(messages=[MessageResponseSchema.model_validate(msg) for msg in messages])
    except Exception as error:
        logger.error(f"Ошибка ендпойнта get_messages: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
