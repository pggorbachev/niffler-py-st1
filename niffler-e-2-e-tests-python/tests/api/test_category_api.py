from clients.category_client import CategoryHttpClient
from databases.spend_db import SpendDb
from marks import TestData
from models.category import CategoryAdd
from models.enum import Categories
import pytest

pytestmark = [pytest.mark.allure_label("Category API", label_type="epic")]


def test_add_new_category(category_client: CategoryHttpClient, spend_db: SpendDb):
    category_name = Categories.TEST_CATEGORY3
    category = category_client.add_category(CategoryAdd(category=category_name, username="oleg"))
    assert category.category == category_name
    assert category.id is not None

    spend_db.delete_category(category.id)


@TestData.category(Categories.TEST_CATEGORY4)
def test_get_all_categories(category, category_client: CategoryHttpClient, spend_db: SpendDb):
    categories = category_client.get_categories()
    assert len(categories) > 0