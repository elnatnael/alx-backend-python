from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import AllowAny
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination  # O

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Conversation.objects.none()
        return Conversation.objects.filter(participants=user).order_by('-created_at')


  ##  def get_queryset(self):
    ##    return Conversation.objects.filter(participants=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participant_ids', [])
        if not participant_ids:
            return Response({"error": "You must provide participant_ids."}, status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participant_ids)
        conversation = Conversation.objects.create()
        conversation.participants.set(participants | User.objects.filter(user_id=request.user.user_id))
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body', 'sender__email']
    filterset_class = MessageFilter
    pagination_class = MessagePagination  # Optional: override global settings

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')  # From nested router
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        if self.request.user not in conversation.participants.all():
            return Response({"detail": "You are not allowed to view messages from this conversation."},
                             status=status.HTTP_403_FORBIDDEN)

        return Message.objects.filter(conversation=conversation).order_by('sent_at')

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        if self.request.user not in conversation.participants.all():
            return Response( {"detail": "You are not allowed to view messages from this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user, conversation=conversation)
