from functools import partial

import requests
from dacite import from_dict

from spotify.api.base import BaseAPI
from spotify.api.models import User


class UserAPI(BaseAPI):
    def me(self) -> User:
        caller = partial(requests.get, f'{self.url}me')

        response = self.process_request(caller)

        return from_dict(data_class=User, data=response)
