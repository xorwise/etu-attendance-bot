from aiogram import Bot, Router, F, types
import os

from aiogram.filters import Command
from aiogram.types import Message

from database import queries
from utils.exceptions import EtuNotFoundException


account_router = Router()
bot = Bot(os.environ.get("BOT_TOKEN", ""))


@account_router.callback_query(F.text == "/logout")
@account_router.message(Command("logout"))
@account_router.message(F.text.casefold() == "logout")
async def command_logout_handler(message: Message):
    try:
        await queries.delete_user(message.chat.id)
        await message.answer(
            "Спасибо, что воспользовались сервисом.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    except EtuNotFoundException as e:
        await message.answer(str(e))
