
from app.bot.keyboards import (
    country_menu, page_menu, sort_menu, time_menu, 
    search_menu, digest_menu, settings_main_menu
)
from app.crud.user_settings import update_user_setting, get_or_create_user_settings
from aiogram.types import CallbackQuery
from aiogram import Router
from typing import Dict, Any, Callable, List
from functools import wraps
from dataclasses import dataclass

router = Router()

@dataclass
class SettingField:
    """Represents a setting field configuration"""
    name: str
    display_func: Callable
    value_parser: Callable = str

@dataclass
class SettingsType:
    """Represents a settings type configuration"""
    icon: str
    title: str
    fields: List[SettingField]
    menu_func: Callable

class SettingsManager:
    """Manages settings configuration and operations"""
    
    def __init__(self):
        self.settings_types = {
            "digest": SettingsType(
                icon="📰",
                title="Digest Settings",
                fields=[
                    SettingField("digest_country", lambda s: f"• Country: {s.digest_country.upper()}"),
                    SettingField("digest_page", lambda s: f"• Page size: {s.digest_page} articles", int)
                ],
                menu_func=digest_menu
            ),
            "search": SettingsType(
                icon="🔍",
                title="Search Settings", 
                fields=[
                    SettingField("search_country", lambda s: f"• Country: {s.search_country.upper()}"),
                    SettingField("search_page", lambda s: f"• Page size: {s.search_page} articles", int),
                    SettingField("sort_by", lambda s: f"• Sort by: {s.sort_by}"),
                    SettingField("time_for_search", lambda s: f"• Time period: {s.time_for_search} days", int)
                ],
                menu_func=search_menu
            )
        }
        
        self.menu_config = {
            "digest_country": ("🌍 Select country for digest news:", lambda: country_menu("digest")),
            "search_country": ("🌍 Select country for search news:", lambda: country_menu("search")),
            "digest_page": ("📄 Select number of articles for digest:", lambda: page_menu("digest")),
            "search_page": ("📄 Select number of articles for search:", lambda: page_menu("search")),
            "search_sort": ("🔀 Select sort option for search results:", lambda: sort_menu()),
            "search_time": ("⏰ Select time period for search:", lambda: time_menu())
        }
    
    def get_settings_text(self, settings_type: str, user_settings: Any, is_update: bool = False) -> str:
        """Generate settings text based on configuration"""
        config = self.settings_types[settings_type]
        title = f"✅ {config.title} Updated!" if is_update else config.title
        
        text = f"{config.icon} <b>{title}</b>\n\n"
        text += "New settings:\n" if is_update else "Current settings:\n"
        
        for field in config.fields:
            text += field.display_func(user_settings) + "\n"
        
        text += "\nSelect another option or go back:" if is_update else "\nSelect an option to change:"
        return text
    
    async def update_setting_and_show_menu(self, callback: CallbackQuery, field: str, value: Any, settings_type: str):
        """Update a setting and show the updated menu"""
        await update_user_setting(callback.from_user.id, field, value)
        user_settings = await get_or_create_user_settings(callback.from_user.id)
        
        text = self.get_settings_text(settings_type, user_settings, is_update=True)
        config = self.settings_types[settings_type]
        
        await callback.message.edit_text(text, reply_markup=config.menu_func())
    
    async def show_menu(self, callback: CallbackQuery, menu_key: str):
        """Show a specific menu based on configuration"""
        if menu_key in self.menu_config:
            text, keyboard_func = self.menu_config[menu_key]
            await callback.message.edit_text(text, reply_markup=keyboard_func())

# Global settings manager instance
settings_manager = SettingsManager()

def error_handler(func: Callable) -> Callable:

    @wraps(func)
    async def wrapper(callback: CallbackQuery, *args, **kwargs):
        try:
            return await func(callback, *args, **kwargs)
        except Exception as e:
            await callback.answer(f"❌ Error: {str(e)}", show_alert=True)
    return wrapper

# Main settings navigation
@router.callback_query(lambda c: c.data == "settings_main")
async def open_main_settings(callback: CallbackQuery):
    await callback.message.edit_text(
        "Chose settings category:",
        reply_markup=settings_main_menu()
    )

@router.callback_query(lambda c: c.data == "settings_search")
async def open_search_settings(callback: CallbackQuery):
    user_settings = await get_or_create_user_settings(callback.from_user.id)
    text = settings_manager.get_settings_text("search", user_settings)
    await callback.message.edit_text(text, reply_markup=search_menu())

@router.callback_query(lambda c: c.data == "settings_digest")
async def open_digest_settings(callback: CallbackQuery):
    user_settings = await get_or_create_user_settings(callback.from_user.id)
    text = settings_manager.get_settings_text("digest", user_settings)
    await callback.message.edit_text(text, reply_markup=digest_menu())

# Generic setting update handlers
@error_handler
async def handle_country_update(callback: CallbackQuery, settings_type: str):
    """Handle country updates for both digest and search"""
    country_code = callback.data.split("_")[-1]
    field = f"{settings_type}_country"
    await settings_manager.update_setting_and_show_menu(callback, field, country_code, settings_type)

@error_handler
async def handle_page_update(callback: CallbackQuery, settings_type: str):
    """Handle page size updates for both digest and search"""
    page_size = int(callback.data.split("_")[-1])
    field = f"{settings_type}_page"
    await settings_manager.update_setting_and_show_menu(callback, field, page_size, settings_type)

@error_handler
async def handle_search_sort_update(callback: CallbackQuery):
    """Handle search sort option updates"""
    sort_option = callback.data.split("_")[-1]
    await settings_manager.update_setting_and_show_menu(callback, "sort_by", sort_option, "search")

@error_handler
async def handle_search_time_update(callback: CallbackQuery):
    """Handle search time period updates"""
    time_hours = int(callback.data.split("_")[-1])
    await settings_manager.update_setting_and_show_menu(callback, "time_for_search", time_hours, "search")

# Country selection handlers
@router.callback_query(lambda c: c.data.startswith("digest_country_"))
async def set_digest_country(callback: CallbackQuery):
    await handle_country_update(callback, "digest")

@router.callback_query(lambda c: c.data.startswith("search_country_"))
async def set_search_country(callback: CallbackQuery):
    await handle_country_update(callback, "search")

# Page size handlers
@router.callback_query(lambda c: c.data.startswith("digest_page_"))
async def set_digest_page(callback: CallbackQuery):
    await handle_page_update(callback, "digest")

@router.callback_query(lambda c: c.data.startswith("search_page_"))
async def set_search_page(callback: CallbackQuery):
    await handle_page_update(callback, "search")

# Sort and time handlers
@router.callback_query(lambda c: c.data.startswith("search_sort_"))
async def set_search_sort(callback: CallbackQuery):
    await handle_search_sort_update(callback)

@router.callback_query(lambda c: c.data.startswith("search_time_"))
async def set_search_time(callback: CallbackQuery):
    await handle_search_time_update(callback)

# Menu navigation handlers
@router.callback_query(lambda c: c.data == "digest_country")
async def show_digest_country_menu(callback: CallbackQuery):
    await settings_manager.show_menu(callback, "digest_country")

@router.callback_query(lambda c: c.data == "search_country")
async def show_search_country_menu(callback: CallbackQuery):
    await settings_manager.show_menu(callback, "search_country")

@router.callback_query(lambda c: c.data == "digest_page")
async def show_digest_page_menu(callback: CallbackQuery):
    await settings_manager.show_menu(callback, "digest_page")

@router.callback_query(lambda c: c.data == "search_page")
async def show_search_page_menu(callback: CallbackQuery):
    await settings_manager.show_menu(callback, "search_page")

@router.callback_query(lambda c: c.data == "search_sort")
async def show_search_sort_menu(callback: CallbackQuery):
    await settings_manager.show_menu(callback, "search_sort")

@router.callback_query(lambda c: c.data == "search_time")
async def show_search_time_menu(callback: CallbackQuery):
    await settings_manager.show_menu(callback, "search_time")
