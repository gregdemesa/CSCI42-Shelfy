from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
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
    
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'user_management/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        context['username'] = self.request.user.username
        return context

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in automatically after signing up
            return redirect('user_management:dashboard')  # Redirect to dashboard/homepage
    else:
        form = UserRegistrationForm()

    return render(request, 'user_management/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('user_management:dashboard')  # Redirect to dashboard
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'login.html')