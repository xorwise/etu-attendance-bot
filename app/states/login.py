from aiogram.fsm.state import State, StatesGroup


class LoginForm(StatesGroup):
    email = State()
    password = State()
