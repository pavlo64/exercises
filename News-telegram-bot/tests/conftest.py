import pytest
from unittest.mock import AsyncMock
from aiogram.types import Message

@pytest.fixture(scope="function")
def anyio_backend():
    return "asyncio"

@pytest.fixture
def mock_message():
    message = AsyncMock(spec=Message)

    message.answer = AsyncMock()
    message.answer_photo = AsyncMock()

    return message


@pytest.fixture
def mock_news():
    return [
        {
            "title": "Title 1",
            "description": "Desc",
            "url": "https://example.com",
            "image_url": None
        }
    ]


@pytest.fixture
def mock_get_headlines(mocker, mock_news):
    return mocker.patch("app.bot.bot.newsapi_client.get_top_headlines", return_value=mock_news)


@pytest.fixture
def mock_send_messages(mocker):
    return mocker.patch("app.bot.bot.send_news_messages", return_value=None)