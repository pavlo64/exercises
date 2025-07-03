from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    news_api_key: str
    BOT_TOKEN: str
    news_api_url: str


    class Config:
        env_file = ".env"

settings = Settings()
