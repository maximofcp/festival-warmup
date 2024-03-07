from abc import ABC, abstractmethod
from typing import Optional

from spotify.api.models import Track
from spotify.api.searches import SearchAPI


class SearchMethod(ABC):
    def __init__(self, search_api: SearchAPI, tracks_per_artist: int):
        self.search_api = search_api
        self.tracks_per_artist = tracks_per_artist

    @abstractmethod
    def search(self, artist_name: str, total_tracks: Optional[int] = None, *args, **kwargs) -> list[Track]:
        ...


class DefaultSearchMethod(SearchMethod):
    def search(self, artist_name: str, total_tracks: Optional[int] = None, *args, **kwargs) -> list[Track]:
        total_tracks = total_tracks or self.tracks_per_artist

        return self.search_api.tracks_by_artist(artist_name, total_tracks)


class PopularitySearchMethod(DefaultSearchMethod):
    def search(self, artist_name: str, *args, **kwargs) -> list[Track]:
        tracks = super().search(artist_name, self.tracks_per_artist * 2, *args, **kwargs)

        return list(sorted(tracks, key=lambda t: t.popularity, reverse=True))[:self.tracks_per_artist]
