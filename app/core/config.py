from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    """Класс для конфигурации настроек приложения через переменные окружения."""
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "messenger"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    class Config:
        """ Конфигурация для загрузки значений из .env файла."""
        env_file = ".env"


setting = Setting()
