from app.services.newsapi_client import NewsAPIClient
from typing import Callable, Awaitable, List, Dict, Any


news_client = NewsAPIClient()

async def get_news(fetch_method: Callable[[], Awaitable[List[Dict[str, Any]]]]) -> List[Dict[str, Any]]:
    articles = await fetch_method()
    if not isinstance(articles, list):
        return "Ошибка: данные не в формате списка статей"
    for i, a in enumerate(articles):
        print(f"[{i}] Type: {type(a)}, Value: {a}")
    return [
        {
            "title": a["title"],
            "description": a.get("description"),
            "url": a["url"],
            "image_url": a.get("urlToImage")
        }
        for a in articles
    ]
