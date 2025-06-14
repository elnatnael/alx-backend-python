# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404,render
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        conversations = Conversation.objects.filter(participants=request.user).order_by('-created_at')
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def create(self, request):
        participant_ids = request.data.get('participant_ids', [])

        if not participant_ids:
            return Response(
                {"error": "You must provide participant_ids."},
                status=status.HTTP_400_BAD_REQUEST
            )

        participants = User.objects.filter(user_id__in=participant_ids)
        conversation = Conversation.objects.create()
        conversation.participants.set(participants | User.objects.filter(user_id=request.user.user_id))  # Add self
        conversation.save()

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, conversation_pk=None):
        conversation = get_object_or_404(Conversation, conversation_id=conversation_pk)

        if request.user not in conversation.participants.all():
            return Response({"detail": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

        messages = conversation.messages.all().order_by('sent_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def create(self, request, conversation_pk=None):
        conversation = get_object_or_404(Conversation, conversation_id=conversation_pk)

        if request.user not in conversation.participants.all():
            return Response({"detail": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            Message.objects.create(
                sender=request.user,
                conversation=conversation,
                message_body=serializer.validated_data['message_body']
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
