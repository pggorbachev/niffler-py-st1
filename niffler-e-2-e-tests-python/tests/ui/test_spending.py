import pytest
from selene import browser

from models.enum import Categories
from models.spend import SpendAdd
from pages.spending_page import spending_page
from marks import Pages, TestData


class TestSpending:

    @Pages.main_page
    def test_spending_title_exists(self):
        spending_page.check_spending_page_titles()

    @pytest.fixture()
    def main_page_late(self, category, spends, envs):
        browser.open(envs.frontend_url)

    @pytest.mark.usefixtures("main_page_late")
    @TestData.category(Categories.TEST_CATEGORY5)
    @TestData.spends(
        SpendAdd(
            amount=108.51,
            description="QA.GURU Python Advanced 1",
            category=Categories.TEST_CATEGORY5,
            spendDate="2024-08-08T18:39:27.955Z",
            currency="RUB"
        )
    )
    def test_create_spending(self, category, spends):
        spending_page.check_spending_exists(Categories.TEST_CATEGORY5, 100)

    @Pages.main_page
    def test_empty_category(self):
        spending_page.create_spending(100, 'RUB', '', 'breakfast')
        spending_page.check_category_error_message()

    @Pages.main_page
    @TestData.category(Categories.TEST_CATEGORY2)
    def test_amount_is_0(self, category):
        spending_page.create_spending(0, 'RUB', f'{Categories.TEST_CATEGORY2}', 'breakfast')
        spending_page.check_amount_error_message()

    @Pages.main_page
    @TestData.category(Categories.TEST_CATEGORY3)
    def test_date_in_future(self, category):
        spending_page.create_spending(100, 'RUB', f'{Categories.TEST_CATEGORY3}', 'breakfast', '2025/12/31')
        spending_page.check_date_error_message()

    @Pages.main_page
    @TestData.category(Categories.TEST_CATEGORY4)
    def test_delete_all_spending(self, category):
        spending_page.create_spending(1000, 'RUB', f'{Categories.TEST_CATEGORY4}', 'breakfast')
        spending_page.check_delete_spending()
