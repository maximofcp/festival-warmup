import json

import requests
from dacite import from_dict
from requests import Response

from spotify.api.errors import APIError
from spotify.api.models import Token


class AuthAPI:
    def __init__(self, code: str, client_id: str, client_secret: str, redirect_uri: str):
        self.code = code
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type: str = "authorization_code"
        self.redirect_uri: str = redirect_uri

    def url(self) -> str:
        return f"https://accounts.spotify.com/api/token?grant_type={self.grant_type}&redirect_uri={self.redirect_uri}&code={self.code}"

    def headers(self) -> dict:
        return {'Content-Type': 'application/x-www-form-urlencoded'}

    def generate_token(self) -> Token:
        response = requests.post(self.url(), headers=self.headers(), auth=(self.client_id, self.client_secret))
        self.checks_errors(response)

        parsed_response = json.loads(response.content)

        return from_dict(data_class=Token, data=parsed_response)

    def refresh_token(self, refresh_token: str) -> Token:
        params = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id}
        response = requests.post(self.url(), data=params, headers=self.headers(),
                                 auth=(self.client_id, self.client_secret))
        self.checks_errors(response)
        parsed_response = json.loads(response.content)

        return from_dict(data_class=Token, data=parsed_response)

    @classmethod
    def checks_errors(cls, response: Response):
        if response.status_code not in (200, 201):
            parsed_response = json.loads(response.content)

            raise APIError(parsed_response['error_description'])
