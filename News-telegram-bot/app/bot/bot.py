from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.core.config import settings
from app.bot.dispatcher import handle_telegram_command
from app.core.config import settings

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("👋 Привет! Я бот новостей. Используйте /digest, /category или /help.")

@dp.message(Command("digest"))
@dp.message(Command("category"))
async def send_news(message: types.Message):
    parts = message.text.split()
    command = parts[0]  # "/digest" или "/category"
    args = parts[1:] if len(parts) > 1 else []

    news_list = await handle_telegram_command(command, args)

    if not news_list:
        await message.answer("❗ Нет новостей.")
        return

    for news in news_list:
        caption = f"<b>{news['title']}</b>\n\n"
        if news.get("description"):
            caption += f"{news['description']}\n\n"
        if news.get("url"):
            caption += f"<a href='{news['url']}'>Читать полностью</a>"

        if news.get("image_url"):
            try:
                await message.answer_photo(
                    photo=news["image_url"],
                    caption=caption,
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"Ошибка при отправке фото: {e}")
                await message.answer(caption)
        else:
            await message.answer(caption)

@dp.message(Command("help"))
async def help_command(message: types.Message):
    text = (
        "<b>📚 Доступные команды:</b>\n"
        "/digest — Последние заголовки\n"
        "/category <code>категория</code> — Новости по категории\n"
        "/help — Помощь\n\n"
        "<b>Примеры категорий:</b> business, entertainment, health, science, sports, technology"
    )
    await message.answer(text)
