from django.db import models
from django.contrib.auth.models import User
from shelfy.models import Media
from hashids import Hashids

hashids = Hashids(salt="your_secret_salt", min_length=6)

class UserLibraryItem(models.Model):
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("dropped", "Dropped"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    
    # 1 to 5 scale
    rating = models.PositiveSmallIntegerField(
        blank=True, null=True, choices=[(i, str(i)) for i in range(1, 6)]
    )
    review = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def get_hashed_id(self):
        return hashids.encode(self.id)

    class Meta:
        unique_together = ("user", "media")

    def __str__(self):
        return f"{self.user.username} - {self.media.title} ({self.status})"