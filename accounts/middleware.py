from .models import App
from django.http import JsonResponse

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_key = request.headers.get("X-API-KEY")

        if not api_key:
            return JsonResponse({"error": "Missing API KEY"}, status=401)
            
        try:
            request.app = App.objects.get(api_key=api_key)
        except App.DoesNotExist:    
            return JsonResponse({"error": "Invalid API KEY"}, status=401)    
        return self.get_response(request)       

        

