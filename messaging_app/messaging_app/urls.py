from django.urls import path, include
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from .views import ConversationViewSet, MessageViewSet

router = SimpleRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

conversation_router = NestedSimpleRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
]
