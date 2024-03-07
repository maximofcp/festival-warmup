from django.contrib.auth.models import User

from spotify.api.users import UserAPI
from spotify.models import SpotifyUser


class UserService:
    def __init__(self, user_api: UserAPI):
        self.user_api = user_api
        self.user = user_api.manager.user

    @classmethod
    def get_spotify_user(cls) -> SpotifyUser:
        return SpotifyUser.objects.get(user=cls.get_admin_user())

    @classmethod
    def get_admin_user(cls) -> SpotifyUser:
        return User.objects.get(username='admin')

    @classmethod
    def get_or_create_spotify_user(cls, code: str) -> SpotifyUser:
        try:
            return cls.get_spotify_user()
        except SpotifyUser.DoesNotExist:
            return SpotifyUser.objects.create(user=cls.get_admin_user(), code=code)

    def sync_spotify_user_with_spotify(self) -> SpotifyUser:
        user = self.user_api.me()

        self.user.external_id = user.id
        self.user.name = user.display_name
        self.user.save()

        return self.user
