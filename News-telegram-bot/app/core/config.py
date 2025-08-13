from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    news_api_key: str
    bot_token: str
    news_api_url: str
    database_url: str

    model_config = ConfigDict(env_file=".env")

settings = Settings()

if settings.database_url.startswith("postgres://"):
    settings.database_url = settings.database_url.replace(
        "postgres://", "postgresql+asyncpg://", 1
    )