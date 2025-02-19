from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    """Класс для конфигурации настроек приложения через переменные окружения."""
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    class Config:
        """ Конфигурация для загрузки значений из .env файла."""
        env_file = ".env"


setting = Setting()
