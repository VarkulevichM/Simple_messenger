# Simple Messenger API

Это простое API для мессенджера, использующее FastAPI, PostgreSQL и Docker. API поддерживает отправку сообщений и получение списка сообщений для чатов.

## Описание проекта

Приложение позволяет пользователям отправлять сообщения в чатах, а также получать список сообщений для определенного чата.

### Основные возможности:
- Отправка сообщений в чат.
- Получение сообщений для чата с пагинацией.
- Поддержка HTTP/2 и HTTP/3 (QUIC).
- Интеграция с Prometheus и Grafana для мониторинга.

## Структура проекта

- **app**: Основной код приложения FastAPI.
  - **api**: Включает маршруты для API.
  - **core**: Конфигурация приложения и метрики.
  - **db**: Модели данных и взаимодействие с базой данных.
  - **schemas**: Описание данных с помощью Pydantic.
  - **services**: Логика бизнес-уровня приложения.
- **nginx**: Конфигурация для NGINX, который работает как обратный прокси с поддержкой HTTP/3.
- **docker-compose.yml**: Конфигурация для запуска приложения и всех зависимостей в Docker.

## Запуск проекта с Docker

Для запуска проекта используем Docker и Docker Compose. Следуйте этим шагам:

### Шаг 1: Клонируйте репозиторий
```bash
git clone https://github.com/yourusername/simple-messenger.git
cd simple-messenger
```
### Шаг 2: Настройка переменных окружения
```
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
POSTGRES_HOST
POSTGRES_PORT
```
### Шаг 3: Запуск проекта
```
docker-compose up --build
```
### Шаг 4: Доступ к API
``` Swagger UI доступен по адресу: ``` https://localhost/docs

```ReDoc доступен по адресу:``` https://localhost/redoc

### Примеры запросов
Отправка сообщения
URL: /api/v1/send_message

Метод: POST

Пример запроса:
```bazaar
{
    "chat_id": 1,
    "user_id": 2,
    "message": "Привет, мир!"
}
```
Ответ:
```bazaar
{
    "chat_id": 1,
    "user_id": 2,
    "message": "Привет, мир!",
    "message_date": "2025-02-19T06:50:18.123456"
}

```
### Получение сообщений
URL: /api/v1/messages

Метод: GET

Пример запроса:

```bazaar
GET /api/v1/messages?chat_id=1&limit=10&offset=0
```
Ответ:
```bazaar
{
    "messages": [
        {
            "chat_id": 1,
            "user_id": 2,
            "message": "Привет, мир!",
            "message_date": "2025-02-19T06:50:18.123456"
        },
        ...
    ]
}
```