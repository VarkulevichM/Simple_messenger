from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import setting
from app.core.log_file import logger
from app.db.models.message import Base
from sqlalchemy.exc import OperationalError
import asyncpg

DATABASE_URL = f"postgresql+asyncpg://{setting.POSTGRES_USER}:{setting.POSTGRES_PASSWORD}@{setting.POSTGRES_HOST}:{setting.POSTGRES_PORT}/{setting.POSTGRES_DB}"


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_database(settings=None):
    """Создаёт базу данных, если она не существует."""
    try:
        conn = await asyncpg.connect(
            user=setting.POSTGRES_USER,
            password=setting.POSTGRES_PASSWORD,
            host=setting.POSTGRES_HOST,
            port=setting.POSTGRES_PORT,
            database="postgres"  # Подключаемся к системной БД
        )
        db_exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", setting.POSTGRES_DB
        )

        if not db_exists:
            await conn.execute(f'CREATE DATABASE "{setting.POSTGRES_DB}" OWNER "{setting.POSTGRES_USER}"')
            logger.info(f"База данных {setting.POSTGRES_DB} успешно создана.")
        else:
            logger.info(f"База данных {setting.POSTGRES_DB} уже существует.")
        await conn.close()
    except Exception as e:
        logger.error(f"Ошибка при создании базы данных: {e}")
        raise


async def init_db():
    """Создаёт все таблицы в базе данных."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Все таблицы успешно созданы.")
    except OperationalError as e:
        logger.error(f"Ошибка при создании таблиц: {e}")
        raise


async def get_db():
    """Получает асинхронную сессию для взаимодействия с базой данных."""
    try:
        async with async_session() as session:
            yield session
    except SQLAlchemyError as error:
        logger.error(f"Ошибка подключения базы данных: {str(error)}")
        raise Exception("Ошибка подключения базы данных") from error
