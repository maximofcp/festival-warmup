import webbrowser

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates spotify user using code"

    def handle(self, *args, **options):
        redirect_uri = settings.REDIRECT_URI
        client_id = settings.CLIENT_ID
        scopes = 'playlist-modify-public playlist-modify-private'
        response_type = 'code'
        url = f'https://accounts.spotify.com/authorize?response_type={response_type}&client_id={client_id}&scope={scopes}&redirect_uri={redirect_uri}'

        webbrowser.open(url)
