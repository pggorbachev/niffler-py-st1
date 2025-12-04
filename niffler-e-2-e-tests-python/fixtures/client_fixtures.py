import pytest
from _pytest.fixtures import FixtureRequest

from models.category import CategoryAdd
from models.config import Envs
from clients.spends_client import SpendsHttpClient
from clients.category_client import CategoryHttpClient
from databases.spend_db import SpendDb
from databases.auth_db import UserDb
from databases.user_db import UserdataDb
from pages.spending_page import spending_page


@pytest.fixture(scope='session')
def spends_client(envs: Envs, auth_api_token: str) -> SpendsHttpClient:
    return SpendsHttpClient(envs, auth_api_token)


@pytest.fixture(scope="session")
def spend_db(envs: Envs) -> SpendDb:
    return SpendDb(envs)


@pytest.fixture(scope="session")
def auth_db(envs: Envs) -> UserDb:
    return UserDb(envs)


@pytest.fixture()
def user_db(envs: Envs) -> UserdataDb:
    return UserdataDb(envs)


@pytest.fixture(scope='session')
def category_client(envs: Envs, auth_api_token: str) -> CategoryHttpClient:
    return CategoryHttpClient(envs, auth_api_token)

@pytest.fixture(params=[])
def category(request: FixtureRequest, category_client: CategoryHttpClient, spend_db: SpendDb):
    category_name = request.param
    category = category_client.add_category(CategoryAdd(category=category_name))
    yield category.category
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def spends(request: FixtureRequest, spends_client: SpendsHttpClient):
    t_spend = spends_client.add_spends(request.param)
    yield t_spend
    all_spends = spends_client.get_spends()
    if t_spend.id in [spend.id for spend in all_spends]:
        spends_client.remove_spends([t_spend.id])


@pytest.fixture()
def delete_spend(request: FixtureRequest, auth: str, envs: Envs):
    name_category = request.param
    yield name_category
    spending_page.delete_spend(name_category)