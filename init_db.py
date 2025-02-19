from app.db.models.message import Base
from app.db.session import engine


def init_db():
    """Создание всех таблиц в базе данных, если они не существуют."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
