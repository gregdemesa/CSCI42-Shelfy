from django.urls import path
from .views import UserShelvesView

app_name = 'shelves'

urlpatterns = [
    path('', UserShelvesView.as_view(), name='user_shelves'),
]