from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def settings_main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Digest Settings", callback_data="settings_digest")],
        [InlineKeyboardButton(text="Search Settings", callback_data="settings_search")],
    ])
    return keyboard


def search_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Search Country", callback_data="search_country")],
        [InlineKeyboardButton(text="Search Page", callback_data="search_page")],
        [InlineKeyboardButton(text="Sort By", callback_data="search_sort")],
        [InlineKeyboardButton(text="Time For Search", callback_data="search_time")],
        [InlineKeyboardButton(text="← Back", callback_data="settings_main")]
    ])
    return keyboard

def digest_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Digest Country", callback_data="digest_country")],
        [InlineKeyboardButton(text="Digest Page", callback_data="digest_page")],
        [InlineKeyboardButton(text="← Back", callback_data="settings_main")]
    ])
    return keyboard

def country_menu(prefix: str):
    """Generate country selection menu for digest or search settings"""
    countries = [
        ("🇺🇸 United States", "us"),
        ("🇬🇧 United Kingdom", "gb"),
        ("🇨🇦 Canada", "ca"),
        ("🇦🇺 Australia", "au"),
        ("🇩🇪 Germany", "de"),
        ("🇫🇷 France", "fr"),
        ("🇮🇹 Italy", "it"),
        ("🇪🇸 Spain", "es"),
        ("🇳🇱 Netherlands", "nl"),
        ("🇸🇪 Sweden", "se"),
        ("🇳🇴 Norway", "no"),
        ("🇩🇪 Switzerland", "ch"),
        ("🇯🇵 Japan", "jp"),
        ("🇰🇷 South Korea", "kr"),
        ("🇮🇳 India", "in"),
        ("🇧🇷 Brazil", "br"),
        ("🇲🇽 Mexico", "mx"),
        ("🇦🇷 Argentina", "ar"),
        ("🇿🇦 South Africa", "za"),
        ("🇷🇺 Russia", "ru"),
        ("🇨🇳 China", "cn"),
    ]
    
    keyboard = []
    for name, code in countries:
        keyboard.append([InlineKeyboardButton(
            text=name, 
            callback_data=f"{prefix}_country_{code}"
        )])
    
    keyboard.append([InlineKeyboardButton(text="← Back", callback_data=f"settings_{prefix}")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def page_menu(prefix: str):
    """Generate page size selection menu"""
    pages = [
        ("5 articles", "5"),
        ("10 articles", "10"),
        ("15 articles", "15"),
        ("20 articles", "20"),
    ]
    
    keyboard = []
    for name, value in pages:
        keyboard.append([InlineKeyboardButton(
            text=name, 
            callback_data=f"{prefix}_page_{value}"
        )])
    
    keyboard.append([InlineKeyboardButton(text="← Back", callback_data=f"settings_{prefix}")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def sort_menu():
    """Generate sort options menu for search"""
    sorts = [
        ("Relevancy", "relevancy"),
        ("Popularity", "popularity"),
        ("Published Date", "publishedAt"),
    ]
    
    keyboard = []
    for name, value in sorts:
        keyboard.append([InlineKeyboardButton(
            text=name, 
            callback_data=f"search_sort_{value}"
        )])
    
    keyboard.append([InlineKeyboardButton(text="← Back", callback_data="settings_search")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def time_menu():
    times = [
        ("1 day", "1"),
        ("3 days", "3"),
        ("1 week", "7"),
        ("1 month", "30"),
        ("3 months", "91"),
        ("6 months", "181"),
        ("1 year", "365"),
    ]
    
    keyboard = []
    for name, value in times:
        keyboard.append([InlineKeyboardButton(
            text=name, 
            callback_data=f"search_time_{value}"
        )])
    
    keyboard.append([InlineKeyboardButton(text="← Back", callback_data="settings_search")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
