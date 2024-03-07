import json
from abc import ABC
from typing import Callable

from requests import Response

from spotify.api.errors import Unauthorized, APIError
from spotify.api.request_manager import RequestManager


class BaseAPI(ABC):
    BASE_URL: str = "https://api.spotify.com/v1/"

    def __init__(self, manager: RequestManager):
        self.manager = manager

    @property
    def url(self) -> str:
        return self.BASE_URL

    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.manager.token.access_token}"}

    def process_request(self, caller: Callable) -> dict:
        with self.manager:
            try:
                return self.handle_response(caller)
            except Unauthorized:
                self.manager.token = self.manager.auth_api.refresh_token(self.manager.token.refresh_token)

                return self.handle_response(caller)

    def handle_response(self, caller) -> dict:
        response = caller(headers=self.headers())
        self.checks_status_errors(response)

        return json.loads(response.content)

    @classmethod
    def checks_status_errors(cls, response: Response):
        if response.status_code == 401:
            raise Unauthorized()
        elif response.status_code >= 400:
            raise APIError(response.content)
