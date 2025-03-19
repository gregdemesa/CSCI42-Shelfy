from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import ProfileForm, UserRegistrationForm
from .models import Profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'user_management/update_profile.html'
    success_url = reverse_lazy('user_management:dashboard')

    def get_object(self, queryset=None):
        return self.request.user.profile

        messages.success(self.request, "Profile updated successfully!") 
        return super().form_valid(form)

class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'user_management/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user) # auto-login after registration
        messages.success(self.request, "Registration successful!")
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('user_management:dashboard')
    
    
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'user_management/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        context['username'] = self.request.user.username
        return context