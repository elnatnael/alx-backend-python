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
        Object-level permission check:
        - obj is a Message instance
        - Check if the request.user is part of the conversation
        """

        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user in obj.conversation.participants.all()

        return False  # Deny all other methods just in case
