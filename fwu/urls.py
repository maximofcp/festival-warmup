from django.urls import path

from . import views

urlpatterns = [
    path("spotify/users/create", views.create_spotify_user, name="create-spotify-user"),
]
