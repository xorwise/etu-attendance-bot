from aiogram import types

from states.callbacks import SubjectCallback

weekdays = {
    "Понедельник": "MON",
    "Вторник": "TUE",
    "Среда": "WED",
    "Четверг": "THU",
    "Пятница": "FRI",
    "Суббота": "SAT",
}


async def days_of_week_kb() -> types.InlineKeyboardMarkup:
    """Function for creating keyboard with days of week

    Returns:
        types.InlineKeyboardMarkup: keyboard with days of week
    """
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    for day in days:
        keyboard.inline_keyboard.append(
            [types.InlineKeyboardButton(text=day, callback_data=weekdays[day])]
        )

    keyboard.inline_keyboard.append(
        [types.InlineKeyboardButton(text="Готово ✨", callback_data="/menu")]
    )
    return keyboard


async def subjects_kb(
    subjects: list[dict], deadlines: list[str]
) -> types.InlineKeyboardMarkup:
    """Function for creating keyboard with subjects

    Args:
        subjects (list[dict]): list of subjects
    Returns:
        types.InlineKeyboardMarkup: keyboard with subjects
    """
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[])
    for subject in subjects:
        if any(deadline.strftime("%H:%M") in subject["time"] for deadline in deadlines):
            keyboard.inline_keyboard.append(
                [
                    types.InlineKeyboardButton(
                        text=subject["name"] + " ✅",
                        callback_data=SubjectCallback(
                            time=subject["time"].replace(":", "-"), name=subject["name"]
                        ).pack(),
                    )
                ]
            )
        else:
            keyboard.inline_keyboard.append(
                [
                    types.InlineKeyboardButton(
                        text=subject["name"],
                        callback_data=SubjectCallback(
                            time=subject["time"].replace(":", "-"), name=subject["name"]
                        ).pack(),
                    )
                ]
            )
    keyboard.inline_keyboard.append(
        [types.InlineKeyboardButton(text="Назад 🔙", callback_data="/subjects")]
    )
    keyboard.inline_keyboard.append(
        [types.InlineKeyboardButton(text="Готово ✨", callback_data="/menu")]
    )

    return keyboard
