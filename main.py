import asyncio
import os
from database import queries
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from handlers.auth import auth_router
from handlers.account import account_router

load_dotenv(".env")
TOKEN = os.environ.get("BOT_TOKEN", None)

dp = Dispatcher()
dp.include_routers(auth_router, account_router)

bot = Bot(TOKEN)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        f"Привет, <b>{hbold(message.from_user.full_name)}</b>!",
        parse_mode=ParseMode.HTML,
    )


async def main() -> None:
    await queries.create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())