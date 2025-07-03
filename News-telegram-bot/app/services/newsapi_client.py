from app.services.http_client import BaseAPIClient
from app.core.config import settings


class NewsAPIClient(BaseAPIClient):
    def __init__(self):
        super().__init__(
            base_url="https://newsapi.org/v2",
            headers={"X-Api-Key": settings.news_api_key}
        )

    async def get_top_headlines(self, country: str = "us", page_size: int = 5, category: str = "general") -> list:
        data = await self.request(
            endpoint="/top-headlines",
            params={"country": country, "pageSize": page_size, "category": category},
        )
        articles =  data.get("articles", [])
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

