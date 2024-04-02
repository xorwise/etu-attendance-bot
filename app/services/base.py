from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
    options = Options()
    options.binary_location = "/bin/chrome-linux64/chrome"
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--start-maximized")

    service = Service("/bin/chromedriver-linux64/chromedriver")

    return webdriver.Chrome(options=options, service=service)


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
    time.sleep(2)

    button = driver.find_element(by="class name", value="btn")
    button.click()

    time.sleep(3)
    driver.get(driver.current_url)
    login_button = driver.find_element(by="xpath", value="//button[@type='submit']")
    login_button.click()

    time.sleep(2)
    if "id.etu.ru" in driver.current_url:
        raise EtuAuthException("Cookies are invalid")

    time.sleep(3)
    rows = driver.find_elements(By.CLASS_NAME, "card-body")
    titles = []
    for row in rows:
        try:
            button = row.find_element(by="xpath", value="//*[text()=' Отметиться ']")
            button.click()
            titles.append(
                row.find_element(By.CLASS_NAME, value="title-3").text.replace("\n", " ")
            )
        except Exception:
            continue
        finally:
            time.sleep(1)

    return titles
