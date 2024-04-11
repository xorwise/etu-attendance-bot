from datetime import datetime
from aiogram import Bot
from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv
from database import queries
import services
import asyncio
from utils.exceptions import EtuAuthException

"""Celery module for ETU attendance"""

load_dotenv(".env")

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.getenv("CELERY_BROKER_URL")
celery_app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")
celery_app.conf.timezone = "Europe/Moscow"
celery_app.conf.beat_schedule = {
    "attend_users-8.00": {
        "task": "worker.attend_users",
        "schedule": crontab(
            minute=0,
            hour=8,
            day_of_week="1-6",
        ),
    },
    "attend_users-9.50": {
        "task": "worker.attend_users",
        "schedule": crontab(
            minute=50,
            hour=9,
            day_of_week="1-6",
        ),
    },
    "attend_users-11.40": {
        "task": "worker.attend_users",
        "schedule": crontab(
            minute=40,
            hour=11,
            day_of_week="1-6",
        ),
    },
    "attend_users-13.40": {
        "task": "worker.attend_users",
        "schedule": crontab(
            minute=40,
            hour=13,
            day_of_week="1-6",
        ),
    },
    "attend_users-15.30": {
        "task": "worker.attend_users",
        "schedule": crontab(
            minute=30,
            hour=15,
            day_of_week="1-6",
        ),
    },
    "attend_users-17.20": {
        "task": "worker.attend_users",
        "schedule": crontab(
            minute=20,
            hour=17,
            day_of_week="1-6",
        ),
    },
}
celery_app.autodiscover_tasks()

weekdays = {
    0: "MON",
    1: "TUE",
    2: "WED",
    3: "THU",
    4: "FRI",
    5: "SAT",
}


async def attend_users_async() -> None:
    """Function for ETU attendance
    checks all users and tries to attend them if cookies are valid
    """
    current_time = datetime.now()
    bot = Bot(os.environ.get("BOT_TOKEN", ""))
    time = current_time.replace(second=0, microsecond=0)
    for user in await queries.users.get_users_by_deadline(
        weekdays[time.weekday()], time.time().strftime("%H:%M")
    ):
        cookies = await queries.cookies.get_cookies_by_user(user.email)
        try:
            subjects = services.base.attend(cookies)
            print(subjects)
            subjects_string = ""
            for subject in subjects:
                subjects_string += f"{subject}\n"

            if len(subjects) > 0:
                await bot.send_message(
                    chat_id=user.id,
                    text=f"Отметились на предметах✅\n{subjects_string}",
                )
        except EtuAuthException:
            await bot.send_message(
                chat_id=user.id,
                text="Сессия личного кабинета истекла❌\nПожалуйста, авторизуйтесь заново с помощью команды /login.",
            )
            await queries.users.delete_user(user.id)
    await bot.session.close()


@celery_app.task
def attend_users() -> None:
    """Celery task for user attendance"""
    asyncio.run(attend_users_async())
