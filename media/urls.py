from django.urls import path
from .views import MediaAPI

urlpatterns = [
    path("search/", MediaAPI.as_view(), name="media_search"),
    path("<str:media_type>/<str:external_id>/", MediaAPI.as_view(), name="media_detail"),
]