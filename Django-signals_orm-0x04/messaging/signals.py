from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

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
        
    
@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()