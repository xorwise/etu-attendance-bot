from aiogram.filters.callback_data import CallbackData


class SubjectCallback(CallbackData, prefix="subject"):
    """Class for subject callback"""

    name: str
    time: str
