from django.http import HttpResponse

from spotify.services.factories import ServiceFactory
from spotify.services.users import UserService


def create_spotify_user(request):
    code = request.GET['code']

    user = UserService.get_or_create_spotify_user(code)
    ServiceFactory.users(user).sync_spotify_user_with_spotify()

    return HttpResponse(f"Welcome, {user.name}! You can close this window now.")
