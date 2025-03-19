from django.urls import path
from .views import LibraryIndexView, AddToLibraryView

app_name = 'user_library'

urlpatterns = [
    path('', LibraryIndexView.as_view(), name='index'),
    path('add/', AddToLibraryView.as_view(), name='add'),
]