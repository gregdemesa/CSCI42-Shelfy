from django.urls import path
from charts import views
from .views import AverageRatingView, MovieCountView

app_name = 'charts'

urlpatterns = [
    path('average-rating', AverageRatingView.as_view(), name='charts'),
    path('movies', MovieCountView.as_view(), name='movie'),
    path('movies-chart', views.movies_chart, name='movies_charts'),
]