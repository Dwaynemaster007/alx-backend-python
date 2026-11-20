from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Message, MessageHistory, Notification

User = get_user_model()


@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """Notify the receiver when a new message arrives."""
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Save the old content to MessageHistory before an edited message is saved."""
    if not instance.pk:
        return
    try:
        original = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return
    if original.content != instance.content:
        MessageHistory.objects.create(
            message=original, old_content=original.content, edited_by=instance.edited_by
        )
        instance.edited = True
        instance.edited_at = timezone.now()


@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """Clean up anything left behind when a user deletes their account.

    The foreign keys already cascade; this makes the clean-up explicit.
    """
    Message.objects.filter(Q(sender=instance) | Q(receiver=instance)).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
