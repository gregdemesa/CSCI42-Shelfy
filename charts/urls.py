from django.urls import path
from .views import AverageRatingView

app_name = 'charts'

urlpatterns = [
    path('average-rating', AverageRatingView.as_view(), name='charts'),
]