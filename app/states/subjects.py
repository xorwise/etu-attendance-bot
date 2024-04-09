from aiogram.fsm.state import State, StatesGroup


class SubjectForm(StatesGroup):
    weekday = State()
    subject = State()
