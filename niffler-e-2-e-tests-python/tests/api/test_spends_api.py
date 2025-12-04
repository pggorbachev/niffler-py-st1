import pytest

from clients.category_client import CategoryHttpClient
from clients.spends_client import SpendsHttpClient
from databases.spend_db import SpendDb
from models.enum import Categories
from models.spend import SpendAdd
from datetime import datetime
from models.spend import Spend
from marks import TestData


pytestmark = [pytest.mark.allure_label("Spends API", label_type="epic")]


def test_auth_token_fixture(auth_api_token):
    assert auth_api_token is not None
    # print(auth_api_token)

@TestData.category(Categories.TEST_CATEGORY5)
def test_add_spend(category_client: CategoryHttpClient, spends_client: SpendsHttpClient, spend_db: SpendDb, category):
    spend_data = SpendAdd(
        amount=108.51,
        description="QA.GURU Python Advanced 2",
        category=category,
        spendDate=datetime.now().strftime("%Y-%m-%d"),
        currency="RUB",
    )

    new_spend = spends_client.add_spends(spend_data)

    assert new_spend.id is not None
    assert new_spend.amount == spend_data.amount

    spend_db.delete_spend(new_spend.id)

@TestData.category(Categories.TEST_CATEGORY5)
def test_add_spend_without_description(category_client: CategoryHttpClient, spends_client: SpendsHttpClient, spend_db: SpendDb, category):
    spend_data = SpendAdd(
        amount=108.51,
        description="",
        category=category,
        spendDate=datetime.now().strftime("%Y-%m-%d"),
        currency="RUB",
    )
    new_spend = spends_client.add_spends(spend_data)

    assert new_spend.category == Categories.TEST_CATEGORY5
    assert new_spend.description == ''

    spend_db.delete_spend(new_spend.id)


@TestData.category(Categories.TEST_CATEGORY5)
def test_add_spend_with_minimal_amount(category_client: CategoryHttpClient, spends_client: SpendsHttpClient, spend_db: SpendDb, category):
    data = SpendAdd(
        amount=0.01,
        description="QA.GURU Python Advanced 2",
        category=category,
        spendDate=datetime.now().strftime("%Y-%m-%d"),
        currency="RUB",
    )
    new_spend = spends_client.add_spends(data)

    assert new_spend.category == Categories.TEST_CATEGORY5
    assert new_spend.amount == 0.01

    spend_db.delete_spend(new_spend.id)


@TestData.category(Categories.TEST_CATEGORY6)
def test_remove_spend(category_client: CategoryHttpClient, spends_client: SpendsHttpClient, spend_db: SpendDb, category):
    data = SpendAdd(
        amount=10500,
        description="QA.GURU Python Advanced 2",
        category=category,
        spendDate=datetime.now().strftime("%Y-%m-%d"),
        currency="RUB",
    )
    new_spend = spends_client.add_spends(data)

    spend_db.delete_spend(new_spend.id)
    response = spends_client.get_spends()
    assert response == []



@TestData.category(Categories.TEST_CATEGORY7)
@TestData.spends(
    SpendAdd(
        amount=108.51,
        description="QA.GURU Python Advanced 2",
        category=Categories.TEST_CATEGORY7,
        spendDate="2024-08-08T18:39:27.955Z",
        currency="RUB",
    )
)
def test_update_spend_description(category_client: CategoryHttpClient, spends_client: SpendsHttpClient, spend_db: SpendDb, category, spends):
    updated_info = Spend(
        id=spends.id,
        spendDate=datetime.now().strftime("%Y-%m-%d"),
        category=category,
        currency="RUB",
        amount=10500,
        description='for test',
        username=spends.username
    )
    updated_spend = spends_client.update_spend(updated_info)
    assert updated_spend.description == 'for test'
    assert updated_spend.username == spends.username


# @TestData.category(Categories.TEST_CATEGORY7)
# @TestData.spends(
#     SpendAdd(
#         amount=108.51,
#         description="QA.GURU Python Advanced 2",
#         category=Categories.TEST_CATEGORY7,
#         spendDate="2024-08-08T18:39:27.955Z",
#         currency="EUR",
#     )
# )
# def test_update_spend_currency_EUR(category, spends, spends_client: SpendsHttpClient, spend_db):
#     updated_info = Spend(
#         id=spends.id,
#         spendDate=datetime.now().strftime("%Y-%m-%d"),
#         category=category,
#         currency="EUR",
#         amount=10500,
#         description='QA.GURU Python Advanced 2',
#         username=spends.username
#     )
#     updated_spend = spends_client.update_spend(updated_info)
#     assert updated_spend.currency == 'EUR'
#     assert updated_spend.username == spends.username
# #
#
# @TestData.category(Categories.TEST_CATEGORY7)
# @TestData.spends(
#     SpendAdd(
#         amount=108.51,
#         description="QA.GURU Python Advanced 2",
#         category=Categories.TEST_CATEGORY7,
#         spendDate="2024-08-08T18:39:27.955Z",
#         currency="RUB",
#     )
# )
# def test_update_spend_currency_KZT(category, spends, spends_client: SpendsHttpClient, spend_db):
#     print(f"Added spend ID: {spends.id}")
#     print(f"spends.username = {spends.username}")
#     updated_info = Spend(
#         id=spends.id,
#         spendDate=datetime.now().strftime("%Y-%m-%d"),
#         category=spends.category,
#         currency="KZT",
#         amount=10500,
#         description='QA.GURU Python Advanced 2',
#         username=spends.username
#     )
#     updated_spend = spends_client.update_spend(updated_info)
#     assert updated_spend.currency == 'KZT'
#     assert updated_spend.username == spends.username