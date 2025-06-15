from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Allow only authenticated users who are participants in the conversation
    to view, create, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Check if user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level check: obj is a Message instance.
        Allow only if the user is a participant in the conversation.
        """
        conversation = obj.conversation  # Assuming message has FK to conversation
        return request.user in conversation.participants.all()
