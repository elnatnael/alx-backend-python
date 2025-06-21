# chats/middleware.py
from datetime import datetime
import os
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.method} {request.path}\n"

        # This resolves to your project root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_path = os.path.join(base_dir, 'requests.log')

        # 🧠 PRINT FOR DEBUGGING
        print("📄 Attempting to log to:", log_path)

        try:
            with open(log_path, 'a') as f:
                f.write(log_message)
        except Exception as e:
            print(f"❌ Error writing log: {e}")

        return self.get_response(request)
    


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        # Allowed time is between 6PM (18:00) and 9PM (21:00)
        if now < datetime.strptime("18:00", "%H:%M").time() or now > datetime.strptime("21:00", "%H:%M").time():
            return HttpResponseForbidden("Access denied: Outside allowed hours (6PM–9PM).")
        return self.get_response(request)