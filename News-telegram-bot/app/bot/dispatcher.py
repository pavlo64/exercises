from app.services.newsapi_client import NewsAPIClient
from app.services.news import get_news

news_client = NewsAPIClient()


async def handle_telegram_command(command: str, args: list[str] = None):
    if command == "/digest":
        return await get_news(news_client.get_top_headlines)

    elif command == "/category":
        if not args:
            return [{
                "title": "❗ Укажите категорию",
                "description": "Например: /category business",
                "url": None,
                "image_url": None
            }]

        category = str(args[0]).lower()
        return await get_news(lambda: news_client.get_by_category(category))

    return [{
        "title": "❗ Команда не распознана",
        "description": "Доступные команды: /digest, /category <category>, /help",
        "url": None,
        "image_url": None
    }]
