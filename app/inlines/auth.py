from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.queries import is_user_present


async def auth_kb(user_id: int) -> InlineKeyboardMarkup:
    if not await is_user_present(user_id):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Авторизоваться👤", callback_data="/login")]
            ]
        )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Удалить аккаунт🗑", callback_data="/logout")]
        ]
    )


async def cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена❌", callback_data="/cancel")]
        ]
    )
