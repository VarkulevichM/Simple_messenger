from app.db.session import engine  # импортируйте ваш async engine
from app.db.models.message import Base
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def init_db():
    # Создание всех таблиц асинхронным способом
    async with engine.begin() as conn:
        # Создание всех таблиц, если их нет
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())
