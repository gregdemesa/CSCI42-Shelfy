from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .api_utils import MediaAPIClient


class MediaSearchView(View):
    def get(self, request):
        query = request.GET.get("q")
        media_type = request.GET.get("media_type", "")

        if not query:
            return render(request, "media/search.html", {"search_results": [], "query": query, "media_type": media_type})

        results = MediaAPIClient.search_media(query, media_type)
        return render(request, "media/search.html", {"search_results": results, "query": query, "media_type": media_type})


class MediaDetailView(View):
    def get(self, request, media_type, external_id):
        details = MediaAPIClient.get_media_details(media_type, external_id)

        if not details:
            return JsonResponse({"error": "Media not found"}, status=404)

        return render(request, "media/media_detail.html", {"media": details, "media_type": media_type, "external_id": external_id})

