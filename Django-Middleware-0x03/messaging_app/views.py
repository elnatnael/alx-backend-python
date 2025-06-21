# messaging_app/views.py

from django.http import HttpResponse

def log_test_view(request):
    return HttpResponse("Log test successful.")
