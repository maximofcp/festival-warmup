from spotify.api.auths import AuthAPI
from spotify.api.models import Token
from spotify.models import SpotifyUser


class RequestManager:
    def __init__(self, auth_api: AuthAPI, user: SpotifyUser):
        self.auth_api = auth_api
        self.user = user
        self.token = Token(access_token=user.access_token, refresh_token=user.refresh_token)

    def __enter__(self):
        if not self.token.access_token:
            token = self.auth_api.generate_token()
            self.token = Token(access_token=token.access_token, refresh_token=token.refresh_token)

    def __exit__(self, *args):
        self.user.access_token = self.token.access_token
        self.user.refresh_token = self.token.refresh_token
        self.user.save()
