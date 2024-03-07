from django.contrib.auth.models import User
from django.db import models

from fwu.models import BaseModel, UpcomingFestival


class SpotifyModel(BaseModel):
    external_id = models.CharField(
        unique=True,
        blank=True,
        null=True,
        max_length=256)

    class Meta:
        abstract = True


class ImageModel(BaseModel):
    url = models.CharField(max_length=1024)
    height = models.IntegerField()
    width = models.IntegerField()

    class Meta:
        abstract = True


class SpotifyUserImage(ImageModel, BaseModel):
    ...


class SpotifyUser(SpotifyModel):
    name = models.CharField(max_length=256)
    email = models.EmailField()
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=False)
    images = models.ForeignKey(
        SpotifyUserImage,
        on_delete=models.SET_NULL,
        null=True)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    code = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class ArtistImage(ImageModel, BaseModel):
    ...


class Artist(SpotifyModel):
    name = models.CharField(max_length=256)
    images = models.ForeignKey(
        ArtistImage,
        on_delete=models.SET_NULL,
        null=True)

    def __str__(self):
        return self.name


class AlbumImage(ImageModel, BaseModel):
    ...


class Album(SpotifyModel):
    name = models.CharField(max_length=256)
    total_tracks = models.IntegerField()
    uri = models.CharField(max_length=256)
    href = models.CharField(max_length=1024)
    release_year = models.IntegerField()
    artist = models.ForeignKey(
        Artist,
        related_name='albums',
        on_delete=models.CASCADE)
    cover = models.ForeignKey(
        AlbumImage,
        on_delete=models.CASCADE,
        null=True,
        related_name='album')

    def __str__(self):
        return self.name


class Track(SpotifyModel):
    name = models.CharField(max_length=256)
    popularity = models.IntegerField()
    uri = models.CharField(max_length=256)
    href = models.CharField(max_length=1024)
    explicit = models.BooleanField()
    duration_ms = models.IntegerField()
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='tracks')

    @property
    def artist(self) -> Artist:
        return self.album.artist

    def __str__(self):
        return self.name


class Playlist(SpotifyModel):
    name = models.CharField(max_length=256)
    uri = models.CharField(max_length=256)
    description = models.CharField(
        max_length=256,
        blank=True,
        null=True)
    tracks = models.ManyToManyField(
        Track,
        related_name='playlists')
    festival = models.ForeignKey(
        UpcomingFestival,
        related_name='playlist',
        on_delete=models.SET_NULL,
        null=True)

    def __str__(self):
        return self.name
