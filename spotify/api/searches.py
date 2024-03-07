from functools import partial

import requests
from dacite import from_dict

from spotify.api.base import BaseAPI
from spotify.api.models import Track


class SearchAPI(BaseAPI):
    @property
    def url(self) -> str:
        return f'{super().url}search'

    def tracks_by_artist(self, artist_name: str, limit: int = 20) -> list[Track]:
        caller = partial(requests.get, f'{self.url}?q=artist:{artist_name}&type=track&limit={limit}')

        response = self.process_request(caller)

        return [from_dict(data_class=Track, data=track) for track in response['tracks']['items']]
