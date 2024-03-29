from handlers.auth import *
from handlers.account import command_logout_handler
from aiogram import Router, F


callback_router = Router()


@callback_router.callback_query(F.data == "/login")
async def login_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    await command_login_handler(callback.message, state)
    await callback.answer()


@callback_router.callback_query(F.data == "/cancel")
async def cancel_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    await command_cancel_handler(callback.message, state)
    await callback.answer()


@callback_router.callback_query(F.data == "/logout")
async def logout_callback_handler(callback: types.CallbackQuery):
    await command_logout_handler(callback.message)
    await callback.answer()
