import time

import pytest
from models.config import Envs
from selene import browser
import allure
from allure_commons.types import AttachmentType
from clients.auth_client import AuthClient


@pytest.fixture(scope='session')
def auth(envs: Envs):
    browser.open(envs.frontend_url)
    browser.element('a:nth-child(1)').click()
    browser.element('input[name=username]').set_value(envs.test_username)
    browser.element('input[name=password]').set_value(envs.test_password)
    browser.element('button[type=submit]').click()
    time.sleep(2)
    token = browser.driver.execute_script('return window.sessionStorage.getItem("id_token")')
    if token is None:
        raise RuntimeError("Не удалось получить токен авторизации")
    allure.attach(token, name="token.txt", attachment_type=AttachmentType.TEXT)
    yield token
    browser.close()


@pytest.fixture(scope="session")
def auth_api_token(envs: Envs):
    token = AuthClient(envs).auth(envs.test_username, envs.test_password)
    if token is None:
        raise RuntimeError("Failed to obtain OAuth token")
    allure.attach(token, name="token.txt", attachment_type=AttachmentType.TEXT)
    return token