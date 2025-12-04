import os

import allure
import pytest
from allure_commons.reporter import AllureReporter
from allure_pytest.listener import AllureListener
from dotenv import load_dotenv
from faker import Faker
from pytest import Item, FixtureDef, FixtureRequest

from clients.auth_client import AuthClient
from clients.kafka_client import KafkaClient
from models.config import Envs
from utils.helper import allure_reporter


pytest_plugins = ["fixtures.auth_fixtures", "fixtures.client_fixtures", "fixtures.pages_fixtures"]


def allure_logger(config) -> AllureReporter:
    listener: AllureListener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, trylast=True)  # hook call after all fixtures
def pytest_runtest_call(item: Item):
    yield
    allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    # Make result visible in fixtures
    setattr(item, "rep_" + rep.when, rep)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_teardown(item):
    yield
    reporter = allure_reporter(item.config)
    test = reporter.get_test(None)
    test.labels = list(filter(lambda x: x.name not in ("tag"), test.labels))


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        profile_url=os.getenv("PROFILE_URL"),
        test_username=os.getenv("USER_NAME"),
        test_password=os.getenv("PASSWORD"),
        kafka_address=os.getenv("KAFKA_ADDRESS"),
        userdata_db_url=os.getenv("USERDATA_DB_URL"),
        auth_db_url=os.getenv("AUTH_DB_URL"),
        registration_url=os.getenv("REGISTRATION_URL"),
        auth_url=os.getenv("AUTH_URL"),
        kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        auth_secret=os.getenv("AUTH_SECRET"),
        logs_file=os.getenv("LOG_FILE"),
    )

@pytest.fixture(scope="session")
def auth_client(envs: Envs):
    return AuthClient(envs)

@pytest.fixture(scope="session")
def kafka(envs):
    # Передавай сюда адрес, например "localhost:9093" или "kafka:9092" в зависимости от окружения
    kafka_servers = envs.kafka_bootstrap_servers
    with KafkaClient(kafka_bootstrap_servers=kafka_servers) as k:
        yield k


@pytest.fixture
def generate_test_user():
    fake = Faker()
    name = fake.user_name()
    password = fake.password()
    return name, password


@pytest.fixture
def generate_category_name():
    fake = Faker()
    return fake.word()
