from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import setting
from app.core.log_file import logger
from app.db.models.message import Base

DATABASE_URL = f"postgresql+asyncpg://{setting.POSTGRES_USER}:{setting.POSTGRES_PASSWORD}@{setting.POSTGRES_HOST}:{setting.POSTGRES_PORT}/{setting.POSTGRES_DB}"


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """Создание базы данных и таблиц в базе данных."""
    try:
        # Шаг 1: Создание базы данных, если она не существует
        async with engine.connect() as conn:
            result = await conn.execute(text(
                f"SELECT 1 FROM pg_database WHERE datname = '{setting.POSTGRES_DB}'"))
            if not result.fetchone():
                # База данных не существует, создаем её
                await conn.execute(text(f"CREATE DATABASE {setting.POSTGRES_DB}"))
                logger.info(
                    f"База данных {setting.POSTGRES_DB} успешно создана.")
            else:
                logger.info(
                    f"База данных {setting.POSTGRES_DB} уже существует.")

        # Шаг 2: Создание таблиц в базе данных
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблицы успешно созданы.")
    except Exception as e:
        logger.error(f"Ошибка при создании базы данных или таблиц: {str(e)}")
        raise Exception("Ошибка при создании базы данных или таблиц") from e


async def get_db():
    """Получает асинхронную сессию для взаимодействия с базой данных."""
    try:
        async with async_session() as session:
            yield session
    except SQLAlchemyError as error:
        logger.error(f"Ошибка подключения базы данных: {str(error)}")
        raise Exception("Ошибка подключения базы данных") from error
