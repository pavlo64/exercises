from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.core.config import settings
from app.services.newsapi_client import NewsAPIClient
from app.schemas.digest_input import CategoryEnum

bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

newsapi_client = NewsAPIClient()

async def send_news_messages(message: Message, news_list):
    for news in news_list:
        caption = f"<b>{news['title']}</b>\n\n"
        if news.get("description"):
            caption += f"{news['description']}\n\n"
        if news.get("url"):
            caption += f"<a href='{news['url']}'>Read full article</a>"

        if news.get("image_url"):
            try:
                await message.answer_photo(
                    photo=news["image_url"],
                    caption=caption,
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Error while sending photo: {e}")
                await message.answer(caption)
        else:
            await message.answer(caption)

@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("👋 Hi! I am news bot. Use /digest or /help.")

@dp.message(Command("digest"))
async def digest_command(message: types.Message):
    parts = message.text.lower().split()
    args = parts[1:] if len(parts) > 1 else ["general"]
    if args[0] not in (item.value for item in CategoryEnum):
        await message.answer("❗ Wrong category. Use /help for more information. ")
        return
    news_list = await newsapi_client.get_top_headlines(category = args[0])

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
    news_list = await newsapi_client.search_news(q = args)

    if not news_list:
        await message.answer("❗There is no news for you.")
        return

    await send_news_messages(message, news_list)


@dp.message(Command("help"))
async def help_command(message: types.Message):
    text = (
        "<b>📚 Available commands:</b>\n\n"
        "/digest — Last news. You can sort them by <code>cateroty</code> \n"
        "<b>Category examples:</b> business, entertainment, health, science, sports, technology\n"
        "/search — You can search news. This command will show top 10 relavant news for last month \n"
        "/help — Help\n"

    )
    await message.answer(text)

@dp.message()
async def fallback_handler(message: types.Message):
    if message.text.startswith("/"):
        await message.answer(
            "❗ Unknown command.\n\n"
            "Available commands:\n"
            "/digest <code>category</code> — Get top news by category\n"
            "/help — Show help and usage information"
        )
