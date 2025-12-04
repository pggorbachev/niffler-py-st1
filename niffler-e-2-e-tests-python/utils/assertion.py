
def check_category_in_db(spend_db, category_id: str, expected_name: str, expected_username: str):
    category = spend_db.get_user_category(category_id)

    assert category is not None
    assert category.category == expected_name
    assert category.username == expected_username


def check_spend_in_db(spend_db, amount: float, category_name: str, description: str, username: str):
    result = spend_db.get_user_spends(username)

    for item in result:
        spend_sql_obj = item[0]
        assert description == spend_sql_obj.description
        assert username == spend_sql_obj.username
        assert amount == spend_sql_obj.amount
        category_sql_obj = item[1]
        assert category_name == category_sql_obj.category


def check_category_name_in_db(spend_db, username: str, target_name: str):
    spends = spend_db.get_user_categories(username)
    categories = []
    for category in spends:
        categories.append(category.category)
    assert target_name in categories
