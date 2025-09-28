"""
Models for the messaging app.
"""
from django.db import models
from django.contrib.auth.models import User
import uuid


class Conversation(models.Model):
    """Model representing a conversation between users."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        participant_names = ", ".join([user.username for user in self.participants.all()[:3]])
        if self.participants.count() > 3:
            participant_names += f" and {self.participants.count() - 3} others"
        return f"Conversation with {participant_names}"


class Message(models.Model):
    """Model representing a message in a conversation."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender.username}: {self.content[:50]}..."

    def save(self, *args, **kwargs):
        """Update conversation's updated_at when saving message."""
        super().save(*args, **kwargs)
        self.conversation.save()  # This will update the updated_at field