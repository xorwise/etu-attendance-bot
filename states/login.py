from aiogram.fsm.state import State, StatesGroup


class LoginForm(StatesGroup):
    email = State()
    password = State()
    message_id = State()
