from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm, CreateProfileForm, UserRegistrationForm
from .models import Profile
from django.contrib.auth.models import User


@login_required
def profile_update(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/homepage')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_update.html', {'form': form})


def profile_create(request):
    if request.method == 'POST':
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/homepage')
    else:
        form = CreateProfileForm()
    return render(request, 'profile_create.html', {'form': form})


def user_create(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/homepage')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard_view(request):
    profile = request.user.profile
    username = request.user.username

    context = {
        'profile': profile,
        'username': username,
    }
    return render(request, 'dashboard.html', context)
