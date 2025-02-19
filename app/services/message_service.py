from app.db.repositories.message_repository import MessageRepository


class MessageService:
    """Сервис для работы с сообщениями. Использует репозиторий для взаимодействия с базой данных."""
    def __init__(self):
        self.repository = MessageRepository()

    async def send_message(self, chat_id: int, user_id: int, message: str):
        """
        Отправляет сообщение в систему.

        :param chat_id: ID чата.
        :param user_id: ID пользователя.
        :param message: Текст сообщения.
        """
        try:
            return await self.repository.create_message(chat_id, user_id, message)
        except Exception as error:
            raise Exception("Не удалось отправить сообщение") from error

    async def get_messages(self, chat_id: int, limit: int = 10, offset: int = 0):
        """
        Получает список сообщений по chat_id.

        :param chat_id: ID чата для получения сообщений.
        :param limit: Максимальное количество сообщений для получения.
        :param offset: Количество сообщений, которые нужно пропустить.
        """
        try:
            return await self.repository.get_messages(chat_id, limit, offset)
        except Exception as error:
            raise Exception("Не удалось получить сообщения") from error

