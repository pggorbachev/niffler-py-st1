import pytest


class Pages:
    main_page = pytest.mark.usefixtures("main_page")
    profile = pytest.mark.usefixtures("profile_page")
    login = pytest.mark.usefixtures("login")
    register = pytest.mark.usefixtures("register")
    delete_spend = lambda name_category: pytest.mark.parametrize("delete_spend", [name_category], indirect=True)


class TestData:
    category = lambda name: pytest.mark.parametrize("category", [name], indirect=True, ids=[name])
    spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param.description)
    category_db = lambda x: pytest.mark.parametrize("category_db", [x], indirect=True, ids=lambda param: param.category)

