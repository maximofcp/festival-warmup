from django.conf import settings

from spotify.api.auths import AuthAPI
from spotify.api.playlists import PlaylistAPI
from spotify.api.request_manager import RequestManager
from spotify.api.searches import SearchAPI
from spotify.api.users import UserAPI
from spotify.models import SpotifyUser
from spotify.services.playlists import PlaylistService
from spotify.services.search import SearchMethod, PopularitySearchMethod
from spotify.services.users import UserService


class ServiceFactory:
    @classmethod
    def search(cls, user: SpotifyUser) -> SearchMethod:
        return PopularitySearchMethod(cls.search_api(user), settings.TRACKS_PER_ARTIST)

    @classmethod
    def playlists(cls, user: SpotifyUser) -> PlaylistService:
        return PlaylistService(cls.search(user), cls.playlist_api(user), settings.TRACKS_PER_ARTIST)

    @classmethod
    def users(cls, user: SpotifyUser) -> UserService:
        return UserService(cls.user_api(user))

    @classmethod
    def auth_api(cls, code: str) -> AuthAPI:
        return AuthAPI(code=code, client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET,
                       redirect_uri=settings.REDIRECT_URI)

    @classmethod
    def playlist_api(cls, user: SpotifyUser) -> PlaylistAPI:
        return PlaylistAPI(cls.request_manager(user))

    @classmethod
    def user_api(cls, user: SpotifyUser) -> UserAPI:
        return UserAPI(cls.request_manager(user))

    @classmethod
    def search_api(cls, user: SpotifyUser) -> SearchAPI:
        return SearchAPI(cls.request_manager(user))

    @classmethod
    def request_manager(cls, user: SpotifyUser) -> RequestManager:
        return RequestManager(cls.auth_api(user.code), user)
