from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import setting
from app.core.log_file import logger
from app.db.models.message import Base
from sqlalchemy.exc import OperationalError

DATABASE_URL = f"postgresql+asyncpg://{setting.POSTGRES_USER}:{setting.POSTGRES_PASSWORD}@{setting.POSTGRES_HOST}:{setting.POSTGRES_PORT}/{setting.POSTGRES_DB}"


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """Создание всех таблиц в базе данных и базы данных, если она не существует."""
    try:
        # Попытка подключения и создания базы данных
        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("База данных и таблицы успешно созданы.")
    except OperationalError as e:
        if 'database "messenger" does not exist' in str(e):
            # Создаем базу данных, если она не существует
            logger.info(f"База данных {setting.POSTGRES_DB} не существует. Создаем её.")
            create_db_url = f"postgresql+asyncpg://{setting.POSTGRES_USER}:{setting.POSTGRES_PASSWORD}@{setting.POSTGRES_HOST}:{setting.POSTGRES_PORT}/postgres"
            create_engine = create_async_engine(create_db_url, echo=True)
            async with create_engine.connect() as conn:
                await conn.execute(f"CREATE DATABASE {setting.POSTGRES_DB}")
            logger.info(f"База данных {setting.POSTGRES_DB} успешно создана.")
            await init_db()  # Попытаться снова создать таблицы в новой базе данных
        else:
            logger.error(f"Ошибка при подключении или создании базы данных: {str(e)}")
            raise Exception("Ошибка при создании базы данных или таблиц") from e


async def get_db():
    """Получает асинхронную сессию для взаимодействия с базой данных."""
    try:
        async with async_session() as session:
            yield session
    except SQLAlchemyError as error:
        logger.error(f"Ошибка подключения базы данных: {str(error)}")
        raise Exception("Ошибка подключения базы данных") from error
