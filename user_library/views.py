from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import UserLibrary
from .forms import UserLibraryForm

class LibraryIndexView(ListView):
    model = UserLibrary
    template_name = 'user_library/index.html'
    context_object_name = 'library'

    def get_queryset(self):
        return UserLibrary.objects.filter(user=self.request.user)

class AddToLibraryView(CreateView):
    model = UserLibrary
    form_class = UserLibraryForm
    template_name = 'user_library/add_to_library.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user_library:index')

class EditLibraryEntryView(UpdateView):
    model = UserLibrary
    form_class = UserLibraryForm
    template_name = 'user_library/edit_library_entry.html'

    def get_queryset(self):
        return UserLibrary.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('user_library:index')

class DeleteLibraryEntryView(DeleteView):
    model = UserLibrary
    template_name = 'user_library/delete_library_entry.html'

    def get_queryset(self):
        return UserLibrary.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('user_library:index')