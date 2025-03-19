from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import UserLibraryItem
from .forms import LibraryItemEditForm
from shelfy.models import Media
from shelfy.api_utils import MediaAPIClient

class LibraryIndexView(LoginRequiredMixin, ListView):
    model = UserLibraryItem
    template_name = "user_library/index.html"
    context_object_name = "library"

    def get_queryset(self):
        return UserLibraryItem.objects.filter(user=self.request.user)


class AddToLibraryView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):        
        media_type = request.POST.get("media_type")
        external_id = request.POST.get("external_id")

        # try to get the media from the database
        media, created = Media.objects.get_or_create(
            external_id=external_id,
            media_type=media_type,
            defaults=self.fetch_and_format_media(media_type, external_id),
        )

        # check if media is already in user library
        if not UserLibraryItem.objects.filter(user=request.user, media=media).exists():
            UserLibraryItem.objects.create(user=request.user, media=media, status="planned")
            messages.success(request, f"{media.title} has been added to your library!")
        else:
            messages.info(request, f"{media.title} is already in your library.")

        return redirect("user_library:index")  # redirect to library index
    
    def fetch_and_format_media(self, media_type, external_id):
        media_data = MediaAPIClient.get_media_details(media_type, external_id)
        
        if "error" in media_data:
            messages.error(self.request, "Failed to retrieve media details from API.")
            return {}

        formatted_data = {
            "title": media_data.get("title"),
            "description": media_data.get("description"),
            "cover_image": media_data.get("cover_image"),
            "release_year": media_data.get("release_year"),
            "genre": media_data.get("genre"),
        }

        if media_type == "book":
            formatted_data["author"] = media_data.get("author")
        elif media_type == "movie":
            formatted_data["director"] = media_data.get("director")
        elif media_type == "game":
            formatted_data["studio"] = media_data.get("studio")

        return formatted_data
    

class EditLibraryItemView(LoginRequiredMixin, UpdateView):
    model = UserLibraryItem
    form_class = LibraryItemEditForm
    template_name = "user_library/edit.html"
    
    def get_success_url(self):
        return reverse_lazy("user_library:index")


@method_decorator(csrf_exempt, name='dispatch')
class UpdateLibraryStatusView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(UserLibraryItem, id=item_id, user=request.user)
        new_status = request.POST.get("status")

        if new_status in dict(UserLibraryItem.STATUS_CHOICES):
            item.status = new_status
            item.save()

            # return updated status + CSRF token for security
            return JsonResponse({
                "success": True,
                "new_status": item.get_status_display(),
                "csrf_token": get_token(request)
            })
        return JsonResponse({"success": False, "error": "Invalid status"}, status=400)

    
class DeleteLibraryItemView(LoginRequiredMixin, View):
    def post(self, request, item_id, *args, **kwargs):
        entry = get_object_or_404(UserLibraryItem, id=item_id, user=request.user)
        entry.delete()
        messages.success(request, "Media removed from your library.")
        return redirect("user_library:index")