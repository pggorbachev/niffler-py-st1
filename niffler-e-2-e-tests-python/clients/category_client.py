import allure
import curlify
import requests
from utils.sessions import BaseSession
from models.config import Envs
from models.category import Category, CategoryAdd
from utils.helper import step

class CategoryHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, envs: Envs, token: str):
        self.session = BaseSession(base_url=envs.gateway_url)
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    @step
    @allure.step('HTTP: get categories')
    def get_categories(self) -> list[Category]:
        response = self.session.get("/api/categories/all")
        # self.raise_for_status(response)
        return [Category.model_validate(item) for item in response.json()]

    @step
    @allure.step('HTTP: add category')
    def add_category(self, category_add: CategoryAdd) -> Category:
        json_data = category_add.model_dump()
        response = self.session.post("/api/categories/add", json=json_data)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to add category: {response.status_code} {response.text}")
        return Category.model_validate(response.json())
