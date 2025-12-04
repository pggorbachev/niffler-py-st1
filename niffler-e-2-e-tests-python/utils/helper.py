from allure_commons.reporter import AllureReporter
from allure_pytest.listener import AllureListener
import os
import types
import datetime
from utils import resource
import allure


@allure.step('DB: check category in db')
def check_category_in_db(spend_db, category_id: str, expected_name: str, expected_username: str,
                         expected_archived: bool):
    category = spend_db.get_user_category(category_id)
    assert category is not None
    assert category.name == expected_name
    assert category.username == expected_username
    assert category.archived == expected_archived


@allure.step('DB: check spend in db')
def check_spend_in_db(spend_db, amount: float, category_name: str, description: str, username: str):
    result = spend_db.get_user_spends(username)

    for item in result:
        spend_sql_obj = item[0]
        assert description == spend_sql_obj.description
        assert username == spend_sql_obj.username
        assert amount == spend_sql_obj.amount
        category_sql_obj = item[1]
        assert category_name == category_sql_obj.name


@allure.step('DB: check category name in db')
def check_category_name_in_db(spend_db, username: str, target_name: str):
    spends = spend_db.get_user_categories(username)
    categories = []
    for category in spends:
        categories.append(category.name)
    assert target_name in categories

def allure_reporter(config) -> AllureReporter:
    listener: AllureListener = next(
        filter(
            lambda plugin: (isinstance(plugin, AllureListener)),
            dict(config.pluginmanager.list_name_plugin()).values(),
        ),
        None,
    )
    return listener.allure_logger

def humanify(name: str):
    import re
    return ' '.join(re.split('_+', name))

def write_log_to_file(data: str):
    log_file = os.getenv('LOG_FILE')
    file_name = (resource.path_log_file(log_file) + ".log")
    with open(file_name, 'a', encoding='utf=8') as logger_file:
        logger_file.write(data + '\n')

def step(fn):
    def fn_with_logging(*args, **kwargs):
        is_method = (
                args
                and isinstance(args[0], object)
                and isinstance(getattr(args[0], fn.__name__), types.MethodType)
        )
        args_to_log = args[1:] if is_method else args
        args_and_kwargs_to_log_as_strings = [
            *map(str, args_to_log),
            *[f'{key}={value}' for key, value in kwargs.items()]
        ]
        args_and_kwargs_string = (
            (': ' + ', '.join(map(str, args_and_kwargs_to_log_as_strings)))
            if args_and_kwargs_to_log_as_strings
            else ''
        )
        write_log_to_file(
            f"\n-----\n"
            + f"Start time: {str(datetime.datetime.now())}\n"
            + '\n'
            + (f'[{args[0].__class__.__name__}] ' if is_method else '')
            + humanify(fn.__name__)
            + args_and_kwargs_string
        )
        return fn(*args, **kwargs)

    return fn_with_logging
