from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse
import os
import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        username = request.user.get_username() if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {username} - Path: {request.method} {request.path}\n"

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_path = os.path.join(base_dir, 'requests.log')

        try:
            with open(log_path, 'a') as f:
                f.write(log_message)
        except Exception as e:
            print(f"Error writing log: {e}")

        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Access denied: Chat allowed only between 6 PM and 9 PM.")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define your list of offensive words
        self.offensive_words = {
            'badword1', 'badword2', 'badword3'  # Add your actual offensive words here
        }

    def __call__(self, request):
        # Skip check for GET requests
        if request.method != 'POST':
            return self.get_response(request)
            
        # Check POST data
        for field, value in request.POST.items():
            if isinstance(value, str):
                lower_value = value.lower()
                if any(bad_word in lower_value for bad_word in self.offensive_words):
                    return JsonResponse(
                        {'error': 'Your message contains inappropriate language'},
                        status=400
                    )
        
        # Check JSON data if applicable
        if request.content_type == 'application/json':
            try:
                data = request.data
                for field, value in data.items():
                    if isinstance(value, str):
                        lower_value = value.lower()
                        if any(bad_word in lower_value for bad_word in self.offensive_words):
                            return JsonResponse(
                                {'error': 'Your message contains inappropriate language'},
                                status=400
                            )
            except:
                pass
                
        return self.get_response(request)

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/api-auth/'):
            return self.get_response(request)

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return self.get_response(request)

        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return HttpResponseForbidden("403 Forbidden: Authentication required.")

        role = getattr(request.user, 'role', None)
        if role not in ['admin', 'host']:
            return HttpResponseForbidden("403 Forbidden: You do not have permission.")

        return self.get_response(request)