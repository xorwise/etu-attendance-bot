from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.exceptions import EtuAuthException
import time

"""Module for ETU attendance"""

names = ["lk_etu_ru_session", "XSRF-TOKEN", "remember_web"]


def create_driver() -> WebDriver:
    """Function for creating webdriver

    Returns:
        WebDriver: webdriver
    """
    grid_url = f"http://{os.getenv('SELENIUM_HOST')}:4444/wd/hub"

    options = Options()
    options.add_argument("--headless")

    return webdriver.Remote(command_executor=grid_url, options=options)


def add_cookies_by_domain(
    driver: WebDriver, cookies: list[dict], domain: str
) -> WebDriver:
    """Function for adding cookies by domain to webdriver

    Args:
        driver (WebDriver): webdriver
        cookies (list[dict]): list of cookies
        domain (str): domain
    Returns:
        WebDriver: webdriver
    """
    present = False
    for cookie in cookies:
        if cookie["domain"] in domain:
            present = True
            driver.add_cookie(cookie)
    if not present:
        raise EtuAuthException("Cookies are invalid")
    return driver


def attend(cookies: list[dict]) -> list[str]:
    """Function for ETU attendance

    Args:
        cookies (list[dict]): list of cookies
    Returns:
        list[str]: list of subject titles that user has just attended
    """
    driver = create_driver()

    driver.get("https://id.etu.ru/")
    driver = add_cookies_by_domain(driver, cookies, "id.etu.ru")

    driver.get("https://lk.etu.ru/")
    driver = add_cookies_by_domain(driver, cookies, "lk.etu.ru")

    driver.get("https://digital.etu.ru/attendance/student")
    time.sleep(1)

    button = driver.find_element(by="class name", value="btn")
    button.click()

    time.sleep(1)
    driver.get(driver.current_url)
    login_button = driver.find_element(by="xpath", value="//button[@type='submit']")
    login_button.click()

    time.sleep(3)
    if "id.etu.ru" in driver.current_url:
        driver.quit()
        raise EtuAuthException("Cookies are invalid")

    rows = driver.find_elements(By.CLASS_NAME, "card-body")
    titles = []
    for row in rows:
        try:
            button = row.find_element(by="xpath", value="//*[text()=' Отметиться ']")
            button.click()
            titles.append(
                " ".join(
                    el.text.replace("\n", " ")
                    for el in row.find_elements(By.CLASS_NAME, value="title-3")
                )
            )
        except Exception:
            continue
    driver.quit()
    return titles
