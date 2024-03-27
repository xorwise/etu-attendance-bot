from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def attend(email: str, password: str) -> str:
    driver = webdriver.Firefox()
    driver.get("https://id.etu.ru/login")
    time.sleep(3)

    username_field = driver.find_element(by="name", value="email")
    password_field = driver.find_element(by="name", value="password")

    login_button = driver.find_element(by="xpath", value="//button[@type='submit']")

    username_field.send_keys(email)
    password_field.send_keys(password)

    login_button.click()

    time.sleep(5)

    try:
        span = driver.find_element(by="class name", value="text-error")
        return span.text
    except Exception:
        pass

    driver.get("https://digital.etu.ru/attendance/auth")
    time.sleep(3)

    button = driver.find_element(by="class name", value="btn")
    button.click()

    time.sleep(3)
    login_button = driver.find_element(by="xpath", value="//button[@type='submit']")
    login_button.click()

    time.sleep(5)

    driver.quit()
    return ""
