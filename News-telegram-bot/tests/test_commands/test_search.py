import pytest
import os
os.environ["BOT_TOKEN"] = "123456:ABCDEF_fake"
os.environ["NEWS_API_KEY"] = "test"
os.environ["NEWS_API_URL"] = "http://test.com"
from unittest.mock import AsyncMock

from app.bot.bot import search_command, send_news_messages


@pytest.mark.asyncio
async def test_search_command_no_args(mock_message):
    mock_message.text = "/search"
    await search_command(mock_message)
    mock_message.answer.assert_awaited_once_with("Please enter search query.")


@pytest.mark.asyncio
async def test_search_command_no_results(mock_message, mocker):
    mocker.patch("app.bot.bot.newsapi_client.search_news", return_value=[])
    mock_message.text = "/search bitcoin"
    await search_command(mock_message)
    mock_message.answer.assert_awaited_once_with("❗There is no news for you.")


@pytest.mark.asyncio
async def test_search_command_with_results(mock_message, mocker):
    fake_news = [{"title": "Title", "description": "Desc", "url": "https://test.com"}]
    mock_search_news = mocker.patch(
        "app.bot.bot.newsapi_client.search_news",
        return_value=fake_news
    )
    mock_send_news = mocker.patch(
        "app.bot.bot.send_news_messages",
        new=AsyncMock()
    )

    mock_message.text = "/search bitcoin"
    await search_command(mock_message)
    mock_search_news.assert_awaited_once_with(q="bitcoin")
    mock_send_news.assert_awaited_once_with(mock_message, fake_news)