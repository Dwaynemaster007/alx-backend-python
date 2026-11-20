from django.conf import settings
from django.db import models

from .managers import UnreadMessagesManager


class Message(models.Model):
    """A direct message. Replies point at their parent to form a thread."""

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, related_name='edited_messages', on_delete=models.SET_NULL
    )
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE
    )

    objects = models.Manager()
    unread = UnreadMessagesManager()

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'

    def get_thread(self):
        """Return this message's replies, nested to any depth, as a list of dicts."""
        replies = Message.objects.filter(parent_message=self).select_related('sender', 'receiver')
        return [{'message': reply, 'replies': reply.get_thread()} for reply in replies]


class Notification(models.Model):
    """Created by a signal whenever a user receives a new message."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Notification for {self.user}'


class MessageHistory(models.Model):
    """The previous content of a message, saved by a signal each time it is edited."""

    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = 'message history'

    def __str__(self):
        return f'Edit of message {self.message_id} at {self.edited_at}'
