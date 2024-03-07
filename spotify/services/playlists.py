from django.conf import settings

from fwu.models import UpcomingFestival
from spotify.api.models import CreatePlaylist
from spotify.api.playlists import PlaylistAPI
from spotify.models import Playlist, Track, Artist, Album, AlbumImage
from spotify.services.search import SearchMethod


class PlaylistService:
    def __init__(self, search_method: SearchMethod, playlist_api: PlaylistAPI, tracks_per_artist: int):
        self.playlist_api = playlist_api
        self.search = search_method
        self.tracks_per_artist = tracks_per_artist
        self.user_id = search_method.search_api.manager.user.external_id

    def create_playlist(self, festival: UpcomingFestival) -> Playlist:
        tracks: list[Track] = []

        for artist_name in festival.artist_names:
            api_tracks = self.search.search(artist_name)

            for track in api_tracks:
                album = track.album

                artists = list(filter(lambda a: artist_name in a.name, album.artists))
                if not artists:
                    continue

                artist = artists[0]

                db_artist, new = Artist.objects.get_or_create(
                    external_id=artist.id,
                    defaults={
                        'name': artist.name,
                    }
                )

                """
                if new:
                    for image in artist.images:
                        ArtistImages.objects.create(
                            url=image.url, width=image.width, height=image.height, artist=db_artist)
                """

                db_album, new = Album.objects.get_or_create(
                    external_id=album.id,
                    defaults={
                        'name': album.name,
                        'total_tracks': album.total_tracks,
                        'uri': album.uri,
                        'href': album.href,
                        'release_year': int(album.release_date[:4]),
                        'artist': db_artist
                    }
                )

                if new and album.images:
                    # pick only the bigger image
                    image = list(sorted(album.images, key=lambda k: k.height, reverse=True))[0]
                    cover = AlbumImage.objects.create(url=image.url, width=image.width, height=image.height)
                    db_album.cover = cover
                    db_album.save()

                db_track, _ = Track.objects.get_or_create(
                    external_id=track.id,
                    defaults={
                        'name': track.name,
                        'popularity': track.popularity,
                        'uri': track.uri,
                        'href': track.href,
                        'explicit': track.explicit,
                        'duration_ms': track.duration_ms,
                        'album': db_album
                    }
                )

                tracks.append(db_track)

        return self._create_playlist_with_tracks(festival, tracks)

    def _create_playlist_with_tracks(self, festival: UpcomingFestival, tracks: list[Track]) -> Playlist:
        api_playlist = self.playlist_api.create_playlist(CreatePlaylist(
            name=self._create_playlist_name(festival),
            description=self._create_playlist_description(festival, tracks),
            public=settings.PUBLIC_PLAYLISTS,
            user_id=self.user_id,
            track_uris=[track.uri for track in tracks]))

        playlist = Playlist.objects.create(
            external_id=api_playlist.id,
            uri=api_playlist.uri,
            name=api_playlist.name,
            description=api_playlist.description,
            festival=festival)
        playlist.tracks.set(tracks)

        return playlist

    @staticmethod
    def _create_playlist_name(festival: UpcomingFestival) -> str:
        return f'{festival.name} {festival.name_mark}'

    @staticmethod
    def _create_playlist_description(festival: UpcomingFestival, tracks: list[Track]) -> str:
        artists = list({t.artist.name for t in tracks})
        description = (f'Auto-generated playlist based on the festival {festival.name}!'
                       f' Featuring artists: {", ".join(artists)}')

        return f'{description[:297]}...'  # description size limit
