from fastapi import HTTPException
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver


def login(email: str, password: str) -> WebDriver:
    options = Options()
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")
    # options.add_argument("--start-maximized")

    driver = webdriver.Chrome()
    driver.get("https://id.etu.ru/login")
    time.sleep(2)

    username_field = driver.find_element(by="name", value="email")
    password_field = driver.find_element(by="name", value="password")

    login_button = driver.find_element(by="xpath", value="//button[@type='submit']")

    username_field.send_keys(email)
    password_field.send_keys(password)

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
        raise HTTPException(status_code=422, detail=text)


def login_lk(email: str, password: str, driver: WebDriver) -> WebDriver:
    driver.get("https://lk.etu.ru/login")
    username_field = driver.find_element(by="name", value="email")
    password_field = driver.find_element(by="name", value="password")
    login_button = driver.find_element(by="xpath", value="//button[@type='submit']")

    username_field.send_keys(email)
    password_field.send_keys(password)

    login_button.click()
    time.sleep(3)
    return driver


def attend(driver: WebDriver):
    driver.get("https://digital.etu.ru/attendance/auth")
    time.sleep(3)

    button = driver.find_element(by="class name", value="btn")
    button.click()

    time.sleep(3)
    login_button = driver.find_element(by="xpath", value="//button[@type='submit']")
    login_button.click()

    time.sleep(3)

    buttons = driver.find_elements(by="xpath", value="//*[text()=' Отметиться ']")

    for button in buttons:
        button.click()
        time.sleep(1)

    driver.quit()
