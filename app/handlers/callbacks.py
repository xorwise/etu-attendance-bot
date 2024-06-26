from handlers.auth import *
from handlers.account import command_logout_handler, command_subjects_handler
from aiogram import Router, F, types

"""Module for callbacks handlers"""


callback_router = Router()


@callback_router.callback_query(F.data == "/login")
async def login_callback_handler(
    callback: types.CallbackQuery, state: FSMContext
) -> None:
    """Handler for /login callback command

    Args:
        callback (types.CallbackQuery): callback
        state (FSMContext): authorization state
    """
    await command_login_handler(callback.message, state)
    await callback.answer()


@callback_router.callback_query(F.data == "/menu")
async def menu_callback_handler(
    callback: types.CallbackQuery, state: FSMContext
) -> None:
    """Handler for /cancel callback command

    Args:
        callback (types.CallbackQuery): callback
        state (FSMContext): authorization state
    """
    await command_menu_handler(callback.message, state)
    await callback.answer()


@callback_router.callback_query(F.data == "/logout")
async def logout_callback_handler(callback: types.CallbackQuery) -> None:
    """Handler for /logout callback command

    Args:
        callback (types.CallbackQuery): callback
    """
    await command_logout_handler(callback.message)
    await callback.answer()


@callback_router.callback_query(F.data == "/subjects")
async def subjects_callback_handler(
    callback: types.CallbackQuery, state: FSMContext
) -> None:
    """Handler for /subjects callback command

    Args:
        callback (types.CallbackQuery): callback
        state (FSMContext): authorization state
    """
    await command_subjects_handler(callback.message, state)
    await callback.answer()
