import json
from json import JSONDecodeError

import allure
import curlify
from allure_commons.types import AttachmentType
from requests import Response


def allure_attach_request(function):
    """Декоратор логироваания запроса, хедеров запроса, хедеров ответа в allure шаг и аллюр аттачмент и в консоль."""

    def wrapper(*args, **kwargs):
        method, url = args[1], args[2]
        from jinja2 import Environment, PackageLoader, select_autoescape
        env = Environment(
            loader=PackageLoader("resources"),
            autoescape=select_autoescape()
        )

        template = env.get_template('colored_request.ftl')

        with allure.step(f"{method} {url}"):
            response: Response = function(*args, **kwargs)

            curl = curlify.to_curl(response.request)

            prepare_render = {
                "request": response.request,
                "curl": curl,
            }
            render = template.render(prepare_render)

            allure.attach(
                body=render,
                name=f"Request",
                attachment_type=AttachmentType.HTML,
                extension=".html"
            )
            try:
                allure.attach(
                    body=json.dumps(response.json(), indent=4).encode("utf8"),
                    name=f"Response json {response.status_code}",
                    attachment_type=AttachmentType.JSON,
                    extension=".html"
                )
            except (JSONDecodeError, TypeError):
                allure.attach(
                    body=response.text.encode("utf8"),
                    name=f"Response text {response.status_code}",
                    attachment_type=AttachmentType.TEXT,
                    extension=".txt")

        return response

    return wrapper