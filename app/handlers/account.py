from aiogram import Bot, Router, F, types
from aiogram.fsm.context import FSMContext
import os
from aiogram.filters import Command
from aiogram.types import Message
from database import queries
from database.queries.users import is_user_present
from states.callbacks import SubjectCallback
from states.subjects import SubjectForm
from utils import etu_api
from utils.exceptions import EtuNotFoundException
import inlines

"""Module for account handlers"""


account_router = Router()
bot = Bot(os.environ.get("BOT_TOKEN", ""))


@account_router.message(Command("logout"))
@account_router.message(F.text.casefold() == "logout")
async def command_logout_handler(message: Message) -> None:
    """Handler for /logout command.

    Args:
        message (Message): message
    """
    try:
        await queries.users.delete_user(message.chat.id)
        await message.answer(
            "Спасибо, что воспользовались сервисом.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    except EtuNotFoundException as e:
        await message.answer(str(e))


@account_router.message(Command("subjects"))
@account_router.message(F.text.casefold() == "subjects")
async def command_subjects_handler(message: Message, state: FSMContext) -> None:
    """Handler for /subjects command.

    Args:
        message (Message): message
        state (FSMContext): state
    """
    user = await queries.users.get_user(message.chat.id)
    if not (await queries.users.is_user_present(user.id)):
        keyboard = await inlines.auth.menu_kb(user.id)
        await message.answer("Меню", reply_markup=keyboard)
        return
    api_id = await queries.groups.get_group_api_id(user.group_id)
    subjects = await etu_api.get_subjects(api_id)
    await state.update_data(subjects=subjects)
    keyboard = await inlines.account.days_of_week_kb()
    await state.set_state(SubjectForm.weekday)
    await message.answer(
        "Меню настройки пар. Здесь вы можете указать, на каких парах вы не хотите, чтобы бот отмечался.\nВыберите день недели.",
        reply_markup=keyboard,
    )


@account_router.callback_query(F.data.in_(["MON", "TUE", "WED", "THU", "FRI", "SAT"]))
async def account_subjects_handler(
    callback: types.CallbackQuery, state: FSMContext
) -> None:
    """Callback handler for weekday choice in subjects settings

    Args:
        callback (types.CallbackQuery): callback
        state (FSMContext): state
    """
    await callback.answer()
    await state.update_data(day=callback.data)
    user = await queries.users.get_user(callback.from_user.id)
    user_deadlines = await queries.users.get_user_deadlines(user.id, callback.data)
    api_id = await queries.groups.get_group_api_id(user.group_id)
    subjects = await etu_api.get_subjects(api_id)
    await state.update_data(subjects=subjects)
    keyboard = await inlines.account.subjects_kb(
        subjects[callback.data], user_deadlines
    )
    await state.set_state("account_subjects")
    await callback.message.edit_text("Выберите пару.", reply_markup=keyboard)


@account_router.callback_query(SubjectCallback.filter())
async def account_subjects_handler(
    callback: types.CallbackQuery, callback_data: SubjectCallback, state: FSMContext
):
    """Callback handler for subject choice in subjects settings

    Args:
        callback (types.CallbackQuery): callback
        callback_data (SubjectCallback): callback data
        state (FSMContext): state
    """
    await callback.answer()
    data = await state.get_data()
    await queries.users.insert_or_delete_user_deadline(
        callback.from_user.id,
        data.get("day"),
        callback_data.time.replace("-", ":"),
    )
    user_deadlines = await queries.users.get_user_deadlines(
        callback.from_user.id, data.get("day")
    )
    keyboard = await inlines.account.subjects_kb(
        data.get("subjects")[data.get("day")],
        user_deadlines,
    )
    await callback.message.edit_text("Выберите пару.", reply_markup=keyboard)
