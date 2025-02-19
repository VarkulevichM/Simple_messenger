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
    """Создание всех таблиц в базе данных."""
    try:
        # создаем все таблицы, если их нет
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("База данных и таблицы успешно созданы.")
    except Exception as e:
        logger.error(f"Ошибка при создании базы данных: {str(e)}")
        raise Exception("Ошибка при создании базы данных") from e


async def get_db():
    """Получает асинхронную сессию для взаимодействия с базой данных."""
    try:
        async with async_session() as session:
            yield session
    except SQLAlchemyError as error:
        logger.error(f"Ошибка подключения базы данных: {str(error)}")
        raise Exception("Ошибка подключения базы данных") from error
