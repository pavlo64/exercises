from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart, Command
from app.core.config import settings
from app.services.newsapi_client import NewsAPIClient
from app.schemas.digest_input import CategoryEnum
from app.schemas.news import Article
from app.bot.keyboards import settings_main_menu
from app.crud.user_settings import get_or_create_user_settings
from app.bot.callbacks import router as callbacks_router

bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

# Include callbacks router
dp.include_router(callbacks_router)

newsapi_client = NewsAPIClient()

async def send_news_messages(message: Message, news_list: list[Article]):
    for news in news_list:
        caption = f"<b>{news.title}</b>\n\n"
        if news.description:
            caption += f"{news.description}\n\n"
        if news.url:
            caption += f"<a href='{news.url}'>Read full article</a>"

        if news.image_url:
            try:
                await message.answer_photo(
                    photo=news.image_url,
                    caption=caption,
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Error while sending photo: {e}")
                await message.answer(caption, parse_mode="HTML")
        else:
            await message.answer(caption, parse_mode="HTML")

@dp.message(CommandStart())
async def start_command(message: Message):
    text = (
        "👋 <b>Welcome to News Bot!</b>\n\n"
        "I will help you stay up to date with the latest news.\n\n"
        "<b>Available commands:</b>\n"
        "/digest — latest news by category\n"
        "/search — search news by keywords\n"
        "/settings — personal preferences\n"
        "/help — help and usage\n\n"
        "Choose an action using the buttons or commands below."
    )
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/digest"), KeyboardButton(text="/search")],
            [KeyboardButton(text="/settings"), KeyboardButton(text="/help")],
        ],
        resize_keyboard=True
    )
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

@dp.message(Command("digest"))
async def digest_command(message: types.Message):
    parts = message.text.lower().split()
    args = parts[1:] if len(parts) > 1 else ["general"]
    if args[0] not in (item.value for item in CategoryEnum):
        await message.answer("❗ Wrong category. Use /help for more information. ")
        return
    
    # Get user settings
    user_settings = await get_or_create_user_settings(message.from_user.id)
    
    news_list = await newsapi_client.get_top_headlines(
        category=args[0],
        country=user_settings.digest_country,
        page_size=user_settings.digest_page,

    )

    if not news_list:
        await message.answer("❗There is no news for you.")
        return

    await send_news_messages(message, news_list)


@dp.message(Command("search"))
async def search_command(message: types.Message):
    parts = message.text.lower().split()
    if len(parts) <= 1:
        await message.answer("Please enter search query.")
        return
    args = parts[1:]
    args = ", ".join(args)
    
    # Get user settings
    user_settings = await get_or_create_user_settings(message.from_user.id)
    
    news_list = await newsapi_client.search_news(
        q=args,
        page_size=user_settings.search_page,
        sortBy=user_settings.sort_by,
        time_for_search=user_settings.time_for_search,
    )

    if not news_list:
        await message.answer("❗There is no news for you.")
        return

    await send_news_messages(message, news_list)


@dp.message(Command("help"))
async def help_command(message: types.Message):
    text = (
        "<b>📚 Available commands:</b>\n\n"
        "/digest — Last news. You can sort them by <code>category</code> \n"
        "<b>Category examples:</b> business, entertainment, health, science, sports, technology\n"
        "/search — You can search news. This command will show top relevant news for last month \n"
        "/settings — Configure your news preferences (country, page size, sort options)\n"
        "/help — Show this help message\n\n"
        "<b>💡 Tip:</b> Use /settings to customize your news experience!"
    )
    await message.answer(text)

@dp.message(Command("settings"))
async def settings_command(message: Message):
    await get_or_create_user_settings(message.from_user.id)
    await message.answer("Выберите категорию настроек:", reply_markup=settings_main_menu())



@dp.message()
async def fallback_handler(message: types.Message):
    if message.text.startswith("/"):
        await message.answer(
            "❗ Unknown command.\n\n"
            "Available commands:\n"
            "/digest <code>category</code> — Get top news by category\n"
            "/help — Show help and usage information"
        )
