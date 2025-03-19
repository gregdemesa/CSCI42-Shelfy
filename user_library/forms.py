from django import forms
from .models import UserLibraryItem

class LibraryItemEditForm(forms.ModelForm):
    class Meta:
        model = UserLibraryItem
        fields = ["status", "rating", "review", "notes"]
    
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        rating = cleaned_data.get("rating")
        review = cleaned_data.get("review")

        # restrict reviews and ratings to only completed or dropped media
        if status not in ["completed", "dropped"]:
            cleaned_data["review"] = None
            cleaned_data["rating"] = None
        
        # optional rating
        if rating == "":
            cleaned_data["rating"] = None

        return cleaned_data