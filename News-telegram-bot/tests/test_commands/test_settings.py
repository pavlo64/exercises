import pytest
from unittest.mock import patch
from app.bot.callbacks import router, open_search_settings, open_digest_settings, set_digest_country, set_search_page, set_search_sort
from app.crud.user_settings import get_or_create_user_settings, update_user_setting


class TestSettingsCallbacks:

    @patch('app.bot.callbacks.get_or_create_user_settings')
    async def test_open_search_settings(self, mock_get_settings, mock_callback_query, mock_user_settings):
        """Test opening search settings menu"""
        mock_get_settings.return_value = mock_user_settings
        mock_callback_query.data = "settings_search"

        await open_search_settings(mock_callback_query)


        mock_callback_query.message.edit_text.assert_called_once()
        call_args = mock_callback_query.message.edit_text.call_args
        text = call_args[0][0]
        
        assert "Search Settings" in text
        assert "GB" in text
        assert "10" in text
        assert "publishedAt" in text
        assert "24" in text

    @patch('app.bot.callbacks.get_or_create_user_settings')
    async def test_open_digest_settings(self, mock_get_settings, mock_callback_query, mock_user_settings):
        """Test opening digest settings menu"""
        mock_get_settings.return_value = mock_user_settings
        mock_callback_query.data = "settings_digest"

        await open_digest_settings(mock_callback_query)

        mock_callback_query.message.edit_text.assert_called_once()
        call_args = mock_callback_query.message.edit_text.call_args
        text = call_args[0][0]
        
        assert "Digest Settings" in text
        assert "US" in text
        assert "5" in text

    @patch('app.bot.callbacks.update_user_setting')
    @patch('app.bot.callbacks.get_or_create_user_settings')
    async def test_set_digest_country(self, mock_get_settings, mock_update_setting, mock_callback_query, mock_user_settings):
        """Test setting digest country"""
        mock_get_settings.return_value = mock_user_settings
        mock_callback_query.data = "digest_country_gb"

        await set_digest_country(mock_callback_query)
        

        mock_update_setting.assert_called_once_with(123456789, "digest_country", "gb")
        
        # Verify the message was edited
        mock_callback_query.message.edit_text.assert_called_once()

    @patch('app.bot.callbacks.update_user_setting')
    @patch('app.bot.callbacks.get_or_create_user_settings')
    async def test_set_search_page(self, mock_get_settings, mock_update_setting, mock_callback_query, mock_user_settings):
        """Test setting search page size"""
        mock_get_settings.return_value = mock_user_settings
        mock_callback_query.data = "search_page_15"

        await set_search_page(mock_callback_query)
        

        mock_update_setting.assert_called_once_with(123456789, "search_page", 15)
        
        # Verify the message was edited
        mock_callback_query.message.edit_text.assert_called_once()

    @patch('app.bot.callbacks.update_user_setting')
    async def test_set_search_sort_error_handling(self, mock_update_setting, mock_callback_query):
        """Test error handling in search sort setting"""
        mock_update_setting.side_effect = ValueError("Invalid sort option")
        mock_callback_query.data = "search_sort_invalid"
        

        await set_search_sort(mock_callback_query)
        
        # Verify error was shown to user
        mock_callback_query.answer.assert_called_once()
        call_args = mock_callback_query.answer.call_args
        assert "Invalid sort option" in call_args[0][0]


class TestUserSettingsCRUD:

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
