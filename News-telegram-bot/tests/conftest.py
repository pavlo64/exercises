import pytest
from unittest.mock import AsyncMock
from types import SimpleNamespace
from app.schemas.news import Article
from aiogram.types import CallbackQuery, Message

@pytest.fixture(scope="function")
def anyio_backend():
    return "asyncio"

@pytest.fixture
def mock_message():
    message = AsyncMock(spec=Message)

    message.answer = AsyncMock()
    message.answer_photo = AsyncMock()
    message.from_user = SimpleNamespace(id=123456789, first_name="Test", username="test_user")

    return message


@pytest.fixture
def mock_news():
    return [Article(title="Image Title", description="Desc", url="https://link.com", image_url="https://img.com/image.jpg")]


@pytest.fixture
def mock_get_headlines(mocker, mock_news):
    return mocker.patch("app.bot.bot.newsapi_client.get_top_headlines", return_value=mock_news)


@pytest.fixture
def mock_send_messages(mocker):
    return mocker.patch("app.bot.bot.send_news_messages", return_value=None)

@pytest.fixture
def mock_callback_query():
    callback = AsyncMock(spec=CallbackQuery)
    callback.from_user = SimpleNamespace(id=123456789, first_name="Test", username="test_user")
    callback.data = "settings_main"

    message_mock = AsyncMock()
    message_mock.edit_text = AsyncMock()
    callback.message = message_mock

    callback.answer = AsyncMock()
    return callback

@pytest.fixture
def mock_user_settings():
    settings = AsyncMock()
    settings.user_id = 123456789
    settings.digest_country = "us"
    settings.digest_page = 5
    settings.search_country = "gb"
    settings.search_page = 10
    settings.sort_by = "publishedAt"
    settings.time_for_search = 24
    return settings