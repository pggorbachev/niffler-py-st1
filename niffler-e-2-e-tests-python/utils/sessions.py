import curlify
import requests
from urllib.parse import parse_qs, urlparse
# from utils.allure_helper import allure_attach_request
from requests import Session
from utils.helper import step


def raise_for_status(function):
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
                raise
        return response

    return wrapper


class BaseSession(Session):
    """Сессия с прокидыванием base_url и логированием запроса, ответа, хедеров ответа."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.base_url = kwargs.pop("base_url", "")

    # @raise_for_status
    # @allure_attach_request
    def request(self, method, url, **kwargs):
        """Логирование запроса и вклейка base_url."""
        return super().request(method, self.base_url + url, **kwargs)


class AuthSession(Session):
    """Сессия с логированием запроса, ответа, хедеров ответа.
    + Авто сохранение cookies внутри сессии из каждого response и redirect response, и 'code' авторизации."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.base_url = kwargs.pop("base_url", "")
        self.code = None

    @step
    # @raise_for_status
    # @allure_attach_request
    def request(self, method, url, **kwargs):
        """Сохраняем cookies, code из редиректа и логируем curl."""

        full_url = self.base_url + url

        # Отделяем параметры для Request и send
        request_kwargs = {k: kwargs[k] for k in ['params', 'data', 'json', 'headers', 'files'] if k in kwargs}
        send_kwargs = {k: kwargs[k] for k in ['timeout', 'allow_redirects', 'proxies', 'stream', 'verify', 'cert'] if
                       k in kwargs}

        # Подготовка запроса
        req = requests.Request(method, full_url, **request_kwargs)
        prep = self.prepare_request(req)

        # Отправляем запрос
        response = super().send(prep, **send_kwargs)

        # Сохраняем куки и code из redirect
        for r in response.history:
            self.cookies.update(r.cookies.get_dict())
            code = parse_qs(urlparse(r.headers.get("Location", "")).query).get("code")
            if code:
                self.code = code[0]

        return response