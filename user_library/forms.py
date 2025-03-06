from django import forms
from .models import UserLibrary
from shelfy.models import Media

class UserLibraryForm(forms.ModelForm):
    class Meta:
        model = UserLibrary
        fields = ['media', 'status', 'rating', 'review']