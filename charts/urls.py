from django.contrib import admin 
from django.urls import path 
# from chartjs import views 
from .views import HomeView, ChartData
  
app_name = 'statistics'

urlpatterns = [ 
    # path('admin/', admin.site.urls), 
    # path('', views.HomeView.as_view()), 
    # path('test-api', views.get_data), 
    path('statistics/view', HomeView.as_view(), name="statistics"), 
] 