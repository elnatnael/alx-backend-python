from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    if instance.id is not None:
        try:
            old_msg = Message.objects.get(id=instance.id)
            if old_msg.content != instance.content:
                instance.edited = True
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_msg.content,
                    edited_by=instance.sender  # or whoever is editing
                )
        except Message.DoesNotExist:
            pass