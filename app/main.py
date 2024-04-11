import asyncio
import os
import database
from database import queries
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import bold
from handlers.auth import auth_router
from handlers.callbacks import callback_router
from handlers.account import account_router
from inlines.auth import menu_kb
from utils import etu_api

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
    keyboard = await menu_kb(message.chat.id)
    await message.answer(
        f"Привет, **{bold(message.from_user.full_name)}**\!\nЯ бот для автоматизации процесса посещаемости в ЛЭТИ\.\nЧтобы начать работу, введите команду /login\.",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=keyboard,
    )


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """Handler for /help command.

    Args:
        message (Message): message
    """
    await message.answer(
        f"**{bold('Посещаемость ЛЭТИ')}**\nДанный телеграм бот создан для автоматизации процесса посещаемости в университете ЛЭТИ\.\nДля начала работы воспользуйтесь командой /login\.\nКаждый учебный день бот будет автоматически отмечаться на парах\.\nИспользуя данного бота, вы берете на себя ответственность за посещение пар\.\nВсе пароли не сохраняются в базе данных\.\nУзать больше \- https://github\.com/xorwise/etu\-attendance\-bot",
        parse_mode=ParseMode.MARKDOWN_V2,
    )


async def main() -> None:
    """Start bot"""
    await database.migrate()
    groups = await etu_api.get_groups()
    await queries.groups.insert_all_groups(groups)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
