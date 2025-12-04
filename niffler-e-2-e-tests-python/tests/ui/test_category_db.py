import os

import pytest

from marks import Pages, TestData
from models.category import CategoryAdd
from models.enum import Information, Categories
from pages.spending_page import spending_page
from utils.assertion import check_category_in_db, check_category_name_in_db, check_spend_in_db
from faker import Faker
from pages.profile_page import profiles_page

fake = Faker()
name = fake.name()

TEST_CATEGORY = "school"

class TestCategoryDb:

    @Pages.profile
    @TestData.category_db(CategoryAdd(
        category=f"Test category name {name}"
    ))
    @pytest.mark.skip
    def test_edit_name_category(self, category_db, spend_db) -> None:
        check_category_in_db(
            spend_db,
            category_db.id,
            category_db.category,
            category_db.username)

        old_name = category_db.category
        new_name = f"{category_db.category} junior"

        profiles_page.edit_category_name(old_name, new_name)
        profiles_page.should_be_category_name(new_name)


    @Pages.profile
    @TestData.category_db(CategoryAdd(
        category=f"Test category name {name}"
    ))
    @pytest.mark.skip
    def test_archived_category(self, category_db, spend_db) -> None:
        check_category_in_db(
            spend_db,
            category_db.id,
            category_db.category,
            category_db.username)

        profiles_page.archive_category(category_db.category)
        profiles_page.check_archived_category(category_db.category)

    @Pages.main_page
    @TestData.category_db(CategoryAdd(
        category=f"Test category name {name}"
    ))
    def test_created_spend_exist_in_database(self, category_db, spend_db):
        user_name = os.getenv("USER_NAME")
        spending_page.create_spending(Information.AMOUNT, 'RUB', category_db, Information.DESCRIPTION)
        check_spend_in_db(spend_db, Information.AMOUNT, category_db, Information.DESCRIPTION, user_name)
        spend_db.delete_spend(category_db.id)


    @Pages.profile
    def test_check_category_name_changes_in_database(self, spend_db):
        user_name = os.getenv("USER_NAME")
        profiles_page.check_adding_category(Categories.TEST_CATEGORY2)
        profiles_page.refresh_page()
        check_category_name_in_db(spend_db, user_name, Categories.TEST_CATEGORY2)