from django.db import models

class Media(models.Model):
    MEDIA_TYPES = [
        ('book', 'Book'),
        ('movie', 'Movie'),
        ('game', 'Game'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    genre = models.CharField(max_length=255, blank=True, null=True)

    author = models.CharField(max_length=255, blank=True, null=True)  # for books
    director = models.CharField(max_length=255, blank=True, null=True)  # for movies
    studio = models.CharField(max_length=255, blank=True, null=True)  # for games

    external_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.title} ({self.media_type})"