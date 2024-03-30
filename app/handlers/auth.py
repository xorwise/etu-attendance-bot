from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database.models import User
from aiogram.filters import Command
from aiogram import F, Router, Bot
from inlines.auth import cancel_kb, auth_kb
from states.login import LoginForm
from aiogram import types
from services import attend
from database import queries
from utils.exceptions import EtuAuthException
from utils.validators import is_valid
from dotenv import load_dotenv
from aiogram.enums import ParseMode
import os

load_dotenv("app/.env")
auth_router = Router()
bot = Bot(os.environ.get("BOT_TOKEN", ""))


@auth_router.callback_query(F.text == "/login")
@auth_router.message(Command("login"))
async def command_login_handler(message: Message, state: FSMContext):
    keyboard = await cancel_kb()
    await state.set_state(LoginForm.email)
    await message.answer("Введите свой Email!", reply_markup=keyboard)


@auth_router.callback_query(F.text == "/cancel")
@auth_router.message(Command("cancel"))
@auth_router.message(F.text.casefold() == "cancel")
async def command_cancel_handler(message: Message, state: FSMContext):
    keyboard = await auth_kb(message.chat.id)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Авторизация отменена", reply_markup=keyboard)


@auth_router.message(LoginForm.email)
async def login_email_handler(message: Message, state: FSMContext):
    keyboard = await cancel_kb()
    if not is_valid(message.text):
        await message.answer(
            "Email введён некорректно\!\nВведите Email в формате **example@example\.com**\!",
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboard,
        )
        return
    await state.update_data(email=message.text)
    await state.set_state(LoginForm.password)
    message2 = await message.answer("Введите свой пароль!", reply_markup=keyboard)
    await state.update_data(message_id=message2.message_id)


@auth_router.message(LoginForm.password)
async def login_password_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    email = data.get("email")
    password = message.text

    message2 = await message.answer("Начинаем проверку...")
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        driver = attend.login(email, password)
        cookies = attend.login_lk(email, password, driver)
        await queries.insert_or_update_user(User(id=message.chat.id, email=email))
        await queries.insert_or_update_cookies(cookies, email)
        keyboard = await auth_kb(message.chat.id)
        await message.answer(
            "Пользователь успешно добавлен в автопосещаемость!", reply_markup=keyboard
        )
        await bot.delete_messages(
            chat_id=message.chat.id,
            message_ids=[
                message2.message_id,
                message.message_id,
                data.get("message_id"),
            ],
        )
    except EtuAuthException as e:
        keyboard = await auth_kb(message.chat.id)
        await message.answer(str(e), reply_markup=keyboard)
    await state.clear()
