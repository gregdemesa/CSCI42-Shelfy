from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from .models import Shelf, ShelfItem
from user_library.models import UserLibraryItem


class UserShelvesView(LoginRequiredMixin, ListView):
    model = Shelf
    template_name = 'shelves/user_shelves.html'
    context_object_name = "shelves"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_library_items = UserLibraryItem.objects.filter(user=self.request.user)
        context["library_items"] = user_library_items
        return context

    def get_queryset(self):
        return Shelf.objects.filter(user=self.request.user)