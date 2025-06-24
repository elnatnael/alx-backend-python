from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # ✅ required field
    read = models.BooleanField(default=False)  # ✅ NEW FIELD
    
    #Managers
    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  # custom manager

    # 👇 Self-referencing foreign key for threading
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.content[:30]}"
    

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='edit_history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)  # ✅ timestamp of edit
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)  # ✅ who edited it

    def __str__(self):
        return f"Edit of message {self.message.id} at {self.edited_at}"



class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


