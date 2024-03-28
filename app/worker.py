from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv

load_dotenv(".env")

celery = Celery(__name__)
celery.conf.broker_url = os.getenv("CELERY_BROKER_URL")
celery.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")


@celery.task
def attend_users():
    from services.attend import attend, login, login_lk
    from database.queries import get_all_users
    import time

    for user in get_all_users():
        try:
            driver = login(user.email, user.password)
            time.sleep(3)
            driver = login_lk(user.email, user.password, driver)
            attend(driver)
            driver.quit()
        except Exception as e:
            print(e)
            continue


celery.autodiscover_tasks()
celery.conf.beat_schedule = {
    "attend_users": {
        "task": "attend_users",
        "schedule": crontab(
            minute=50,
            hour="8, 9, 11, 13, 15, 17",
            day_of_week="mon,tue,wed,thu,fri,sat",
        ),
    }
}

celery.conf.timezone = "Europe/Moscow"
