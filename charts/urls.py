from django.urls import path 
from .views import HomeView, ChartData
  
app_name = 'statistics'

urlpatterns = [ 
    # path('admin/', admin.site.urls), 
    path('statistics/', HomeView.as_view(), name="statistics_home"), 
    # path('test-api', views.get_data), 
    # path('statistics/chart', ChartData.as_view(), name="statistics"), 
] 