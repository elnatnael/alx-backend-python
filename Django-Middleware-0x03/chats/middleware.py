from datetime import datetime
from django.http import HttpResponseForbidden
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

        print("📄 Attempting to log to:", log_path)

        try:
            with open(log_path, 'a') as f:
                f.write(log_message)
            print("✅ Log written successfully")
        except Exception as e:
            print(f"❌ Error writing log: {e}")

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
        # Dictionary to track IPs: { ip_address: [(timestamp1), (timestamp2), ...] }
        self.ip_message_times = {}

    def __call__(self, request):
        # Only count POST requests (assuming messages are sent via POST)
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()

            # Initialize the list if IP not tracked yet
            if ip not in self.ip_message_times:
                self.ip_message_times[ip] = []

            # Remove timestamps older than 60 seconds (1 minute window)
            one_minute_ago = now - 60
            self.ip_message_times[ip] = [t for t in self.ip_message_times[ip] if t > one_minute_ago]

            # Check if IP exceeded 5 messages in the last minute
            if len(self.ip_message_times[ip]) >= 5:
                return HttpResponseForbidden("Message limit exceeded: max 5 messages per minute.")

            # Record this message timestamp
            self.ip_message_times[ip].append(now)

        # Continue processing the request
        return self.get_response(request)

    def get_client_ip(self, request):
        # Standard way to get IP from request headers
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip



class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"🔍 Incoming {request.method} to {request.path}")

        """ if request.path.startswith('/admin/') or request.path.startswith('/api-auth/'):
           return self.get_response(request)
         """
        # ✅ Allow safe methods
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            print("✅ Allowed: Safe method")
            return self.get_response(request)

        # ✅ Check if user is authenticated
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            print("❌ Blocked: Not authenticated")
            return HttpResponseForbidden("403 Forbidden: Authentication required.")

        # ✅ Check if user has admin or host role
        role = getattr(request.user, 'role', None)
        print(f"👤 Role: {role}")
        if role not in ['admin', 'host']:
            print("❌ Blocked: Role not allowed")
            return HttpResponseForbidden("403 Forbidden: You do not have permission.")

        print("✅ Allowed: Authorized user")
        return self.get_response(request)

