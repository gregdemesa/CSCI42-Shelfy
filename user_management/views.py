from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm, UserRegistrationForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'user_management/update_profile.html'
    success_url = reverse_lazy('user_management:update_profile')

    def get_object(self, queryset=None):
        return self.request.user.profile


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'user_management/register.html'
    success_url = reverse_lazy('login')  # redirect to login after registration

    def form_valid(self, form):
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'user_management/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        context['username'] = self.request.user.username
        return context