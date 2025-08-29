from app.services.http_client import BaseAPIClient
from app.core.config import settings
from app.schemas.news import Article
import logging
import datetime
from dateutil.relativedelta import relativedelta



async def create_news_list(data) -> list[Article]:
    articles = data.get("articles", [])
    if not isinstance(articles, list):
        logging.error("Wrong data format: articles is not a list")
        return []
    for i, a in enumerate(articles):
        logging.debug(f"[{i}] Article received: {a}")
    result = []
    for i,a in enumerate(articles):
        logging.debug(f"[{i}] Article received: {a}")
        try:
            result.append(
                Article(
                    title=a["title"],
                    description=a.get("description"),
                    url=a["url"],
                    image_url=a.get("image_url"),
                )
            )
        except KeyError as e:
            logging.warning(f"Article is skipped because field is missing {e}")
    return result

class NewsAPIClient(BaseAPIClient):
    def __init__(self):
        super().__init__(
            base_url=settings.news_api_url,
            headers={"X-Api-Key": settings.news_api_key}
        )

    async def get_top_headlines(self, country: str = "us", page_size: int = 5, category: str = "general") -> list:
        data = await self.request(
            endpoint="/top-headlines",
            params={"country": country, "pageSize": page_size, "category": category},
        )
        return await create_news_list(data)

    async def search_news(self,q:str, page_size: int = 10, sortBy:str = "relevancy", time_for_search:str = '30' ) -> list:
        search_from = datetime.date.today() - relativedelta(days=int(time_for_search))
        data = await self.request(
            endpoint="/everything",
            params={ "pageSize": page_size, "sortBy": sortBy,"from":search_from, "q":q },
        )
        return await create_news_list(data)