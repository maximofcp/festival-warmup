from django.contrib import admin, messages
from django.utils.html import escape, format_html

from fwu.models import UpcomingFestival
from spotify.models import SpotifyUser, Artist, Album, Track, Playlist
from spotify.services.factories import ServiceFactory
from spotify.services.users import UserService


class ViewOnlyMixin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class TrackAdmin(ViewOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'album', 'artist')
    readonly_fields = ('external_id', 'name', 'popularity', 'uri', 'href', 'explicit', 'duration_ms', 'album')


class SpotifyUserAdmin(ViewOnlyMixin, admin.ModelAdmin):
    list_display = ('name',)
    fields = ('external_id', 'name', 'email', 'user', 'images')


class TrackInline(admin.TabularInline):
    model = Track.playlists.through
    fields = ('artist', 'name', 'album')
    readonly_fields = ('artist', 'name', 'album')
    verbose_name = 'Track'
    extra = 0

    def artist(self, obj):
        return obj.track.artist.name
    artist.short_description = 'Artist'

    def name(self, obj):
        return obj.track.name
    name.short_description = 'Track'

    def album(self, obj):
        return obj.track.album.name
    album.short_description = 'Album'


class PlaylistAdmin(ViewOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'festival', 'get_song_count')
    fields = ('external_id', 'name', 'description', 'tracks', 'festival')
    inlines = (TrackInline,)

    def has_delete_permission(self, request, obj=None):
        return True

    def get_song_count(self, obj) -> int:
        return obj.tracks.count()

    get_song_count.short_description = 'Total songs'


class ArtistAdmin(ViewOnlyMixin, admin.ModelAdmin):
    list_display = ('name', 'get_album_count')
    readonly_fields = ('external_id', 'name', 'images')

    def get_album_count(self, obj) -> int:
        return obj.albums.count()

    get_album_count.short_description = 'Total albums'


class AlbumAdmin(ViewOnlyMixin, admin.ModelAdmin):
    list_display = ('show_cover_list', 'name', 'artist', 'release_year', 'total_tracks')
    readonly_fields = (
        'show_cover_edit', 'external_id', 'name', 'total_tracks', 'uri', 'href', 'release_year', 'artist')

    def show_cover_list(self, obj):
        return format_html(f'<img src="{escape(obj.cover.url)}" width="150" height="150" />')

    show_cover_list.short_description = 'Cover'
    show_cover_list.allow_tags = True

    def show_cover_edit(self, obj):
        return format_html(f'<img src="{escape(obj.cover.url)}" />')

    show_cover_edit.short_description = 'Cover'
    show_cover_edit.allow_tags = True


class UpcomingFestivalAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    fields = ('name', 'description', 'year', 'artists')
    actions = ("create_playlist",)

    @admin.action(description='Create playlist for the selected upcoming festivals')
    def create_playlist(modeladmin, request, queryset):
        user = UserService.get_spotify_user()
        festivals = queryset.filter(playlist__isnull=True)
        if not festivals.count():
            messages.warning(request, f'Festival(s) selected already have a playlist associated.')
            return

        for festival in festivals:
            playlist = ServiceFactory.playlists(user).create_playlist(festival)
            messages.success(request, f'Created playlist {playlist}!')


admin.site.register(SpotifyUser, SpotifyUserAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(UpcomingFestival, UpcomingFestivalAdmin)
