from django.core.management.base import BaseCommand

from fwu.models import UpcomingFestival
from spotify.services.factories import ServiceFactory
from spotify.services.users import UserService


class Command(BaseCommand):
    help = "Creates spotify user using code"

    def handle(self, *args, **options):
        user = UserService.get_spotify_user()

        festivals = UpcomingFestival.objects.filter(playlist__isnull=True)

        for festival in festivals:
            playlist = ServiceFactory.playlists(user).create_playlist(festival)
            self.stdout.write(f'Created playlist {playlist}')
