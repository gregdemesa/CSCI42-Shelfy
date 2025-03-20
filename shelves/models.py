from django.db import models
from django.contrib.auth.models import User
from user_management.models import Profile
from user_library.models import UserLibraryItem

class Shelf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shelves")
    name = models.CharField(max_length=255, blank=True)
    is_public = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.name:
            if hasattr(self.user, 'profile') and self.user.profile.display_name:
                self.name = f"{self.user.profile.display_name}'s Shelf"
            else:
                self.name = f"{self.user.username}'s Shelf"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ShelfItem(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(UserLibraryItem, on_delete=models.CASCADE)

    # each ShelfItem has the same ID as the corresponding UserLibraryItem
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.item.id
        super().save(*args, **kwargs)
   
    def __str__(self):
        return f"{self.item.media.title} on {self.shelf.name}"