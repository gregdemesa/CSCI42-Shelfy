from django.urls import path
from .views import ProfileUpdateView, DashboardView, register
from django.contrib.auth import views as auth_views

app_name = 'user_management'

urlpatterns = [
    path('profile/', ProfileUpdateView.as_view(), name='update_profile'),
    path('register/', register, name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]