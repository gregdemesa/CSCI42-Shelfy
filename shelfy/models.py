from django.db import models
from user_management.models import Profile

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
    
class Comment(models.Model):
    comment_author = models.ForeignKey(Profile, null = True,on_delete= models.SET_NULL, related_name = "media_comment_author" )
    media = models.ForeignKey(Media, on_delete = models.CASCADE)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True) #https://www.scaler.com/topics/django/django-datetimefield/ \        
    
    def __str__(self):
        return self.entry
    
    class Meta:
        ordering = ['-created_on'] 