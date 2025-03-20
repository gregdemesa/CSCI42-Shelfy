from django.urls import path
from .views import update_profile, register, dashboard 
from django.contrib.auth import views as auth_views

app_name = 'user_management'

urlpatterns = [
    path('profile/', update_profile, name='update_profile'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]