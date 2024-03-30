from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from utils.exceptions import EtuAuthException


class MyDriver:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


def create_driver() -> WebDriver:
    options = Options()
    options.binary_location = "/app/app/bin/chrome-linux64/chrome"
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--start-maximized")

    service = Service("/app/app/bin/chromedriver")

    return webdriver.Chrome(service=service, options=options)


def login(email: str | None, password: str | None) -> WebDriver:
    driver = create_driver()
    driver.get("https://id.etu.ru/login")
    time.sleep(2)

    username_field = driver.find_element(by="name", value="email")
    password_field = driver.find_element(by="name", value="password")

    login_button = driver.find_element(by="xpath", value="//button[@type='submit']")
    checkbox = driver.find_element(by="id", value="remember")

    username_field.send_keys(email)
    password_field.send_keys(password)
    checkbox.click()

    login_button.click()

    time.sleep(1)
    text = ""
    try:
        span = driver.find_element(by="class name", value="text-error")
        text = span.text
    except Exception:
        return driver
    else:
        driver.quit()
        raise EtuAuthException(text)


def login_lk(email: str, password: str, driver: WebDriver) -> list[dict]:
    driver.get("https://lk.etu.ru/login")
    username_field = driver.find_element(by="name", value="email")
    password_field = driver.find_element(by="name", value="password")
    login_button = driver.find_element(by="xpath", value="//button[@type='submit']")

    username_field.send_keys(email)
    password_field.send_keys(password)

    login_button.click()
    time.sleep(3)
    return driver.get_cookies()


def attend(cookies: list[dict]) -> list[str]:

    my_driver = MyDriver(create_driver())
    with my_driver as driver:
        id_cookie = {}
        lk_cookie = {}
        for cookie in cookies:
            if cookie["domain"] in "id.etu.ru":
                id_cookie = cookie
            elif cookie["domain"] in "lk.etu.ru":
                lk_cookie = cookie
        if not id_cookie or not lk_cookie:
            raise EtuAuthException("Cookies are invalid")

        driver.get("https://id.etu.ru/")
        driver.add_cookie(id_cookie)

        driver.get("https://lk.etu.ru/")
        driver.add_cookie(lk_cookie)

        driver.get("https://digital.etu.ru/attendance/auth")
        time.sleep(2)

        button = driver.find_element(by="class name", value="btn")
        button.click()

        time.sleep(3)
        login_button = driver.find_element(by="xpath", value="//button[@type='submit']")
        login_button.click()

        time.sleep(3)
        if "id.etu.ru" in driver.current_url:
            raise EtuAuthException("Cookies are invalid")

        rows = driver.find_elements(by="class name", value="card-body")
        titles = []
        for row in rows:
            try:
                button = row.find_element(
                    by="xpath", value="//*[text()=' Отметиться ']"
                )
                button.click()
                titles.append(
                    " ".join(
                        el.text
                        for el in row.find_elements(by="class name", value="card-title")
                    )
                )
                time.sleep(1)
            except Exception:
                continue
        return titles
