import pytest
from selene import browser
from models.config import Envs
from urllib.parse import urljoin
# from selenium.webdriver.chrome.options import Options


@pytest.fixture()
def profile_page(auth: str, envs: Envs):
    return browser.open(envs.profile_url)


@pytest.fixture()
def main_page(auth: str, envs: Envs):
    browser.open(envs.frontend_url)

@pytest.fixture()
def login(envs: Envs):
    login = urljoin(envs.frontend_url, "/login")
    return browser.open(login)

@pytest.fixture()
def register(envs: Envs):
    return browser.open(envs.registration_url)



# добавление авторизации в браузер
# @pytest.fixture()
# def main_page(auth_api_token: str, envs: Envs):
#     # Необязательная часть
#     # options = Options()
#     # # options.add_argument("--headless")
#     # options.add_argument("--start-maximized")
#     # options.add_argument("--disable-site-isolation-trials")  # Отключает изоляцию сайтов
#     # options.add_argument("--allow-file-access-from-files")  # Разрешает доступ к файлам
#     # # options.add_argument("--disable-redirects")
#     # options.add_argument("--remote-debugging-port=9222")  # Включаем DevTools
#     #
#     # browser.config.driver_options = options
#     # browser.config.timeout = 10
#     # Обязательная часть
#     browser.driver.execute_cdp_cmd(
#         "Page.addScriptToEvaluateOnNewDocument",
#         {"source": f"localStorage.setItem('id_token', '{auth_api_token}');"}
#     )
#     browser.driver.refresh()
#     browser.open(envs.frontend_url)