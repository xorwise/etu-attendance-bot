from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.queries.users import is_user_present

"""Module for auth inlines"""


async def menu_kb(user_id: int) -> InlineKeyboardMarkup:
    """Function for creating auth keyboard
    if user is present it creates /logout button otherwise creates /login

    Args:
        user_id (int): user id
    Returns:
        InlineKeyboardMarkup: auth keyboard
    """
    if not await is_user_present(user_id):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Авторизоваться👤", callback_data="/login")]
            ]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Настроить предметы📚", callback_data="/subjects"
                )
            ],
            [InlineKeyboardButton(text="Удалить аккаунт🗑", callback_data="/logout")],
        ]
    )


async def cancel_kb() -> InlineKeyboardMarkup:
    """Function for creating cancel keyboard

    Returns:
        InlineKeyboardMarkup: cancel keyboard
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Отмена❌", callback_data="/menu")]]
    )
