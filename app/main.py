import asyncio
import os
from database import queries
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from handlers.auth import auth_router
from handlers.callbacks import callback_router
from handlers.account import account_router
from inlines.auth import auth_kb

"""Main module with bot startup logic"""

load_dotenv("app/.env")
TOKEN = os.environ.get("BOT_TOKEN", None)

dp = Dispatcher()
dp.include_routers(auth_router, account_router, callback_router)

bot = Bot(TOKEN)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    """Handler for /start command.

    Args:
        message (Message): message
    """
    keyboard = await auth_kb(message.chat.id)
    await message.answer(
        f"""
        Привет, <b>{hbold(message.from_user.full_name)}</b>!
        Я бот для автоматизации процесса посещаемости в ЛЭТИ.
        Чтобы начать работу, введите команду /login.
        """,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """Handler for /help command.

    Args:
        message (Message): message
    """
    await message.answer(
        """
    <b>Посещаемость ЛЭТИ</b>
    Данный телеграм бот создан для автоматизации процесса посещаемости в университете ЛЭТИ.
    Для начала работы воспользуйтесь командой /login.
    Каждый будний день бот будет автоматически отмечаться на парах.
    Используя данного бота, вы берете на себя ответственность за посещение пар.
    Все пароли не сохраняются в базе данных.

    Узать больше - https://github.com/xorwise/etu-attendance-bot
    """,
        parse_mode=ParseMode.HTML,
    )


async def main() -> None:
    """Start bot"""
    await queries.create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
