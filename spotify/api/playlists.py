import json
from functools import partial

import requests
from dacite import from_dict

from spotify.api.base import BaseAPI
from spotify.api.models import CreatePlaylist, Playlist
from spotify.utils import chunks


class PlaylistAPI(BaseAPI):
    uri_limit = 100  # stated in documentation

    def headers(self) -> dict:
        return {**super().headers(), 'Content-Type': 'application/json'}

    def create_playlist(self, request: CreatePlaylist) -> Playlist:
        data = {'name': request.name, 'description': request.description, 'public': request.public}
        url = f'{super().url}users/{request.user_id}/playlists'

        caller = partial(requests.post, url, json=data)
        response = self.process_request(caller)

        playlist = from_dict(data_class=Playlist, data=response)

        self.add_tracks(playlist.id, request.track_uris)

        return playlist

    def add_tracks(self, playlist_id: str, track_uris: list[str]) -> None:
        uri_chunks = chunks(track_uris, self.uri_limit)

        for chunk in uri_chunks:
            data = {'uris': chunk, 'position': 0}
            url = f'{super().url}playlists/{playlist_id}/tracks'

            requests.post(url, data=json.dumps(data), headers=self.headers())
