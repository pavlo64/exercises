from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NEWS_API_KEY: str
    BOT_TOKEN: str

    class Config:
        env_file = ".env"

settings = Settings()
