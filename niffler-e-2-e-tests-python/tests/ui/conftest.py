import pytest
from clients.category_client import CategoryHttpClient
from databases.spend_db import SpendDb
from _pytest.fixtures import FixtureRequest

@pytest.fixture()
def category_db(request: FixtureRequest, category_client: CategoryHttpClient, spend_db: SpendDb):
    category = category_client.add_category(request.param)
    yield category
    spend_db.delete_category(category.id)