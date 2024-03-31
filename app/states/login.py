from aiogram.fsm.state import State, StatesGroup

"""Module for login states"""


class LoginForm(StatesGroup):
    """Login form states"""

    email = State()
    password = State()
    message_id = State()
