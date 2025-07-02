
from app.services.newsapi_client import NewsAPIClient
from app.services.news_service import get_news

news_client = NewsAPIClient()

commands_registry = {
    "/latest": {
        "description": "Последние новости",
        "handler": lambda: get_news(news_client.get_top_headlines)
    },
    "/category": {
        "description": "Новости по категории (по умолчанию general)",
        "handler": lambda: get_news(lambda: news_client.get_by_category("general"))
    }
}