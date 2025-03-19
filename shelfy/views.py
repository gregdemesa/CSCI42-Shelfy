from django.http import JsonResponse
from django.views import View
from .api_utils import MediaAPIClient

class MediaSearchView(View):
    """
    Handles searching for books, movies, and games.
    """

    def get(self, request, media_type=None):
        query = request.GET.get("q")
        if not query:
            return JsonResponse({"error": "Query parameter 'q' is required."}, status=400)

        results = MediaAPIClient.search_media(query, media_type)
        return JsonResponse({"results": results})


class MediaDetailView(View):
    """
    Fetches detailed information for a specific media item.
    """

    def get(self, request, media_type, external_id):
        details = MediaAPIClient.get_media_details(media_type, external_id)
        return JsonResponse(details)
