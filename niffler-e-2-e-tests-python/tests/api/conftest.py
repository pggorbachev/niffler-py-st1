import pytest
from models.config import Envs
from pages.spending_page import spending_page
from clients.spends_client import SpendsHttpClient
from clients.category_client import CategoryHttpClient
from databases.spend_db import SpendDb
from models.category import CategoryAdd
from _pytest.fixtures import FixtureRequest


