from selenium.webdriver.chrome.webdriver import WebDriver
from services.base import create_driver
import time
from utils.exceptions import EtuAuthException

"""Module for ETU authorization"""


def login(email: str | None, password: str | None) -> WebDriver:
    """Function for id.etu.ru authorization
    function also checks "remember me" checkbox

    Args:
        email (str): provided email
        password (str): provided password
    Returns:
        WebDriver: webdriver
    """
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
    """Function for lk.etu.ru authorization

    Args:
        email (str): provided email
        password (str): provided password
        driver (WebDriver): webdriver
    Returns:
        list[dict]: list of cookies
    """
    driver.get("https://lk.etu.ru/login")
    username_field = driver.find_element(by="name", value="email")
    password_field = driver.find_element(by="name", value="password")
    login_button = driver.find_element(by="xpath", value="//button[@type='submit']")

    username_field.send_keys(email)
    password_field.send_keys(password)

    login_button.click()
    time.sleep(3)
    return driver.get_cookies()
