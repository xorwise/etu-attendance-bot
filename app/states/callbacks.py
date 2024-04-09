from aiogram.filters.callback_data import CallbackData


class SubjectCallback(CallbackData, prefix="subject"):
    name: str
    time: str
