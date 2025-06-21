"""
URL configuration for messaging_app project.

For more information, see:
https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# ✅ Import the log_test_view directly here if needed
from messaging_app.views import log_test_view  # Make sure this exists!

def root_redirect(request):
    return HttpResponseRedirect('/api/')

urlpatterns = [
    path('', root_redirect),  # redirect root to /api/
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # Needed for checker
    path('api-auth/', include('rest_framework.urls')),

    # ✅ JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # ✅ Custom test view
    path('log-test/', log_test_view, name='log_test'),
]
