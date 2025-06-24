from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class MessageSignalTest(TestCase):
    def test_notification_created_on_message(self):
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')

        msg = Message.objects.create(sender=user1, receiver=user2, content='Test Message')
        self.assertTrue(Notification.objects.filter(user=user2, message=msg).exists())
