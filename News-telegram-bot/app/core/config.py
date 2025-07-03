from pydantic import BaseSettings

class Settings(BaseSettings):
    news_api_key: str
    bot_token: str
    news_api_url: str


    class Config:
        env_file = ".env"

settings = Settings()
