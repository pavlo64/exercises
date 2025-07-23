import pytest
import os

os.environ["BOT_TOKEN"] = "123456:ABCDEF_fake"
os.environ["NEWS_API_KEY"] = "test"
os.environ["NEWS_API_URL"] = "http://test.com"

from app.bot.bot import digest_command, send_news_messages
from app.schemas.digest_input import CategoryEnum


@pytest.mark.asyncio
async def test_digest_valid_category(mock_message, mock_get_headlines, mock_send_messages):
    mock_message.text = "/digest technology"
    await digest_command(mock_message)
    mock_send_messages.assert_awaited_once_with(mock_message, mock_get_headlines.return_value)

@pytest.mark.asyncio
async def test_digest_invalid_category(mock_message):
    mock_message.text = "/digest unknown"
    await digest_command(mock_message)
    mock_message.answer.assert_awaited_once_with("❗ Wrong category. Use /help for more information. ")

@pytest.mark.asyncio
async def test_digest_default_category_used(mock_message, mock_get_headlines, mock_send_messages):
    mock_message.text = "/digest"
    await digest_command(mock_message)
    mock_send_messages.assert_awaited_once_with(mock_message, mock_get_headlines.return_value)

@pytest.mark.asyncio
async def test_digest_no_news_found(mock_message, mocker):
    mock_message.text = "/digest technology"
    mocker.patch("app.bot.bot.newsapi_client.get_top_headlines", return_value=[])
    await digest_command(mock_message)
    mock_message.answer.assert_awaited_once_with("❗There is no news for you.")

@pytest.mark.asyncio
async def test_send_news_with_image(mock_message):
    news = [{
        "title": "Image Title",
        "description": "Desc",
        "url": "https://link.com",
        "image_url": "https://img.com/image.jpg"
    }]
    await send_news_messages(mock_message, news)
    mock_message.answer_photo.assert_awaited_once()
    mock_message.answer.assert_not_awaited()

@pytest.mark.asyncio
async def test_send_news_image_error_fallback_to_answer(mock_message):
    news = [{
        "title": "Title",
        "description": "Desc",
        "url": "https://url.com",
        "image_url": "https://img.com/image.jpg"
    }]
    mock_message.answer_photo.side_effect = Exception("Network error")
    await send_news_messages(mock_message, news)
    mock_message.answer.assert_awaited_once()
