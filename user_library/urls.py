from django.urls import path
from .views import LibraryIndexView, AddToLibraryView, EditLibraryEntryView, DeleteLibraryEntryView

app_name = 'user_library'

urlpatterns = [
    path('', LibraryIndexView.as_view(), name='index'),
    path('add/', AddToLibraryView.as_view(), name='add'),
    path('edit/<int:pk>/', EditLibraryEntryView.as_view(), name='edit'),
    path('delete/<int:pk>/', DeleteLibraryEntryView.as_view(), name='delete'),
]