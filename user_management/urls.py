from django.urls import path
from .views import ProfileUpdateView, UserRegistrationView, DashboardView

app_name = 'user_management'

urlpatterns = [
    path('profile/', ProfileUpdateView.as_view(), name='update_profile'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]