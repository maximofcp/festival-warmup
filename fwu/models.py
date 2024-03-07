import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False)

    class Meta:
        abstract = True


class UpcomingFestival(BaseModel):
    name = models.CharField(max_length=256)
    description = models.TextField(
        blank=True,
        null=True)
    year = models.IntegerField()
    artists = models.TextField()

    @property
    def name_mark(self) -> str:
        return '[fwu]'

    @property
    def artist_names(self) -> list[str]:
        return [artist.strip() for artist in self.artists.split(',')]

    def __str__(self):
        return self.name
