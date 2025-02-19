from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.db.models.message import Message
from app.db.session import async_session


class MessageRepository:
    """Репозиторий для работы с сообщениями в базе данных."""
    async def create_message(self, chat_id: int, user_id: int,message: str) -> Message:
        """
        Создает новое сообщение и сохраняет его в базе данных.

        :param chat_id: ID чата, в котором будет сохранено сообщение.
        :param user_id: ID пользователя, который отправляет сообщение.
        :param message: Текст сообщения.
        """
        try:
            async with async_session() as session:
                new_message = Message(
                    chat_id=chat_id,
                    user_id=user_id,
                    message=message
                )
                session.add(new_message)
                await session.commit()
                await session.refresh(new_message)
                return new_message
        except SQLAlchemyError as error:
            await session.rollback()
            raise Exception("Ошибка связанная с записью") from error

    async def get_messages(self, chat_id: int, limit: int = 10, offset: int = 0) -> list[Message]:
        """
        Получает список сообщений из базы данных по указанному chat_id.

        :param chat_id: ID чата для получения сообщений.
        :param limit: Максимальное количество сообщений для получения.
        :param offset: Количество сообщений, которые нужно пропустить.
        """
        try:
            async with async_session() as session:
                query = select(Message).where(Message.chat_id == chat_id).limit(limit).offset(offset)
                result = await session.execute(query)
                return result.scalars().all()
        except SQLAlchemyError as error:
            raise Exception("Ошибка при выборке") from error
