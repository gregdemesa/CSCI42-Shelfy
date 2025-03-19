from django.urls import path
from .views import LibraryIndexView, AddToLibraryView, EditLibraryItemView, UpdateLibraryStatusView

app_name = 'user_library'

urlpatterns = [
    path('', LibraryIndexView.as_view(), name='index'),
    path('add/', AddToLibraryView.as_view(), name='add'),
    path('edit/<int:pk>', EditLibraryItemView.as_view(), name='edit'),
    path('update/<int:item_id>/', UpdateLibraryStatusView.as_view(), name='update-status'),
]