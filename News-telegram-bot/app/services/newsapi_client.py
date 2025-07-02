from app.services.http_client import BaseAPIClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class NewsAPIClient(BaseAPIClient):
    def __init__(self):
        super().__init__(
            base_url="https://newsapi.org/v2",
            headers={"X-Api-Key": settings.NEWS_API_KEY}
        )

    async def get_top_headlines(self, country: str = "us", page_size: int = 5):
        data = await self.request(
            endpoint="/top-headlines",
            params={"country": country, "pageSize": page_size}
        )
        return data.get("articles", [])

    async def get_by_category(self, category: str, country: str = "us",page_size: int = 5):
        try:
            data = await self.request(
                endpoint="/top-headlines",
                params={
                    "country": country,
                    "pageSize": page_size,
                    "category": category,
                },
            )

            if isinstance(data, dict) and isinstance(data.get("articles"), list):
                return data["articles"]

            logger.warning(f"Unexpected response format: {data}")
            return []

        except Exception as e:
            logger.error(f"Failed to get news by category '{category}': {e}")
            return []