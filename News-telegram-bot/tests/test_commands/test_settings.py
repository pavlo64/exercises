import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import CallbackQuery, Message, User
from app.bot.callbacks import router
from app.crud.user_settings import get_or_create_user_settings, update_user_setting


@pytest.fixture
def mock_callback_query():
    """Create a mock callback query for testing"""
    callback = AsyncMock(spec=CallbackQuery)
    callback.from_user.id = 12345
    callback.data = "settings_main"
    callback.message.edit_text = AsyncMock()
    callback.answer = AsyncMock()
    return callback


@pytest.fixture
def mock_user_settings():
    """Create mock user settings"""
    settings = AsyncMock()
    settings.user_id = 12345
    settings.digest_country = "us"
    settings.digest_page = 5
    settings.search_country = "gb"
    settings.search_page = 10
    settings.sort_by = "publishedAt"
    settings.time_for_search = 24
    return settings


class TestSettingsCallbacks:
    """Test settings callback handlers"""

    @patch('app.bot.callbacks.get_or_create_user_settings')
    async def test_open_search_settings(self, mock_get_settings, mock_callback_query, mock_user_settings):
        """Test opening search settings menu"""
        mock_get_settings.return_value = mock_user_settings
        mock_callback_query.data = "settings_search"
        
        # Get the handler
        handler = router.callback_query(lambda c: c.data == "settings_search")
        
        # Execute the handler
        await handler(mock_callback_query)
        
        # Verify the message was edited with correct text
        mock_callback_query.message.edit_text.assert_called_once()
        call_args = mock_callback_query.message.edit_text.call_args
        text = call_args[0][0]
        
        assert "Search Settings" in text
        assert "US" in text  # digest_country
        assert "GB" in text  # search_country
        assert "5" in text   # digest_page
        assert "10" in text  # search_page
        assert "publishedAt" in text
        assert "24" in text  # time_for_search

    @patch('app.bot.callbacks.get_or_create_user_settings')
    async def test_open_digest_settings(self, mock_get_settings, mock_callback_query, mock_user_settings):
        """Test opening digest settings menu"""
        mock_get_settings.return_value = mock_user_settings
        mock_callback_query.data = "settings_digest"
        
        # Get the handler
        handler = router.callback_query(lambda c: c.data == "settings_digest")
        
        # Execute the handler
        await handler(mock_callback_query)
        
        # Verify the message was edited with correct text
        mock_callback_query.message.edit_text.assert_called_once()
        call_args = mock_callback_query.message.edit_text.call_args
        text = call_args[0][0]
        
        assert "Digest Settings" in text
        assert "US" in text  # digest_country
        assert "5" in text   # digest_page

    @patch('app.bot.callbacks.update_user_setting')
    @patch('app.bot.callbacks.get_or_create_user_settings')
    async def test_set_digest_country(self, mock_get_settings, mock_update_setting, mock_callback_query, mock_user_settings):
        """Test setting digest country"""
        mock_get_settings.return_value = mock_user_settings
        mock_callback_query.data = "digest_country_gb"
        
        # Get the handler
        handler = router.callback_query(lambda c: c.data.startswith("digest_country_"))
        
        # Execute the handler
        await handler(mock_callback_query)
        
        # Verify update was called with correct parameters
        mock_update_setting.assert_called_once_with(12345, "digest_country", "gb")
        
        # Verify the message was edited
        mock_callback_query.message.edit_text.assert_called_once()

    @patch('app.bot.callbacks.update_user_setting')
    @patch('app.bot.callbacks.get_or_create_user_settings')
    async def test_set_search_page(self, mock_get_settings, mock_update_setting, mock_callback_query, mock_user_settings):
        """Test setting search page size"""
        mock_get_settings.return_value = mock_user_settings
        mock_callback_query.data = "search_page_15"
        
        # Get the handler
        handler = router.callback_query(lambda c: c.data.startswith("search_page_"))
        
        # Execute the handler
        await handler(mock_callback_query)
        
        # Verify update was called with correct parameters
        mock_update_setting.assert_called_once_with(12345, "search_page", 15)
        
        # Verify the message was edited
        mock_callback_query.message.edit_text.assert_called_once()

    @patch('app.bot.callbacks.update_user_setting')
    async def test_set_search_sort_error_handling(self, mock_update_setting, mock_callback_query):
        """Test error handling in search sort setting"""
        mock_update_setting.side_effect = ValueError("Invalid sort option")
        mock_callback_query.data = "search_sort_invalid"
        
        # Get the handler
        handler = router.callback_query(lambda c: c.data.startswith("search_sort_"))
        
        # Execute the handler
        await handler(mock_callback_query)
        
        # Verify error was shown to user
        mock_callback_query.answer.assert_called_once()
        call_args = mock_callback_query.answer.call_args
        assert "Error updating setting" in call_args[0][0]


class TestUserSettingsCRUD:
    """Test user settings CRUD operations"""

    @patch('app.crud.user_settings.async_session')
    async def test_update_user_setting_validation(self, mock_session):
        """Test validation in update_user_setting"""
        # Test invalid field
        with pytest.raises(ValueError, match="Invalid field"):
            await update_user_setting(12345, "invalid_field", "value")
        
        # Test invalid page size
        with pytest.raises(ValueError, match="Page size must be between"):
            await update_user_setting(12345, "digest_page", 0)
        
        # Test invalid country code
        with pytest.raises(ValueError, match="Country code must be 2 characters"):
            await update_user_setting(12345, "digest_country", "invalid")
        
        # Test invalid sort option
        with pytest.raises(ValueError, match="Sort option must be one of"):
            await update_user_setting(12345, "sort_by", "invalid_sort") 