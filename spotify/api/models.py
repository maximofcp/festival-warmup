from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Token:
    access_token: Optional[str] = field(default=None)
    refresh_token: Optional[str] = field(default=None)


@dataclass
class Image:
    url: str
    height: int
    width: int


@dataclass
class User:
    id: str
    display_name: str
    images: list[Image]


@dataclass
class Artist:
    id: str
    name: str


@dataclass
class Album:
    id: str
    name: str
    total_tracks: int
    href: str
    uri: str
    release_date: str
    images: list[Image]
    artists: list[Artist]


@dataclass
class Track:
    id: str
    name: str
    popularity: int
    uri: str
    href: str
    explicit: bool
    duration_ms: int
    album: Album


@dataclass
class Playlist:
    id: str
    name: str
    description: str
    uri: str


@dataclass
class CreatePlaylist:
    name: str
    description: str
    public: bool
    user_id: str
    track_uris: list[str]
