"""
Custom permission classes for the messaging app.
"""
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    
    def has_permission(self, request, view):
        """Check if user is authenticated."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if user is a participant in the conversation."""
        # For Message objects
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(id=request.user.id).exists()
        
        # For Conversation objects
        if hasattr(obj, 'participants'):
            return obj.participants.filter(id=request.user.id).exists()
        
        return False


class IsOwnerOrParticipant(BasePermission):
    """
    Permission to allow message owners or conversation participants to access.
    """
    
    def has_permission(self, request, view):
        """Check if user is authenticated."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check permissions based on the action."""
        # For Message objects
        if hasattr(obj, 'sender'):
            # Owner can always access their messages
            if obj.sender == request.user:
                return True
            
            # Participants can view messages in their conversations
            if hasattr(obj, 'conversation'):
                return obj.conversation.participants.filter(id=request.user.id).exists()
        
        # For Conversation objects
        if hasattr(obj, 'participants'):
            return obj.participants.filter(id=request.user.id).exists()
        
        return False


class IsMessageOwner(BasePermission):
    """
    Permission to only allow message owners to edit/delete their messages.
    """
    
    def has_permission(self, request, view):
        """Check if user is authenticated."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if user is the message owner."""
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        return False


class CanCreateConversation(BasePermission):
    """
    Permission to allow authenticated users to create conversations.
    """
    
    def has_permission(self, request, view):
        """Check if user is authenticated."""
        return request.user and request.user.is_authenticated


class CanSendMessage(BasePermission):
    """
    Permission to allow participants to send messages in a conversation.
    """
    
    def has_permission(self, request, view):
        """Check if user is authenticated."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if user can send messages in the conversation."""
        # For creating messages, check if user is a participant
        conversation_id = request.data.get('conversation') or getattr(obj, 'conversation_id', None)
        
        if conversation_id:
            from .models import Conversation
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                return conversation.participants.filter(id=request.user.id).exists()
            except Conversation.DoesNotExist:
                return False
        
        return False


# Combined permission classes for different use cases
class ConversationPermissions(IsAuthenticated):
    """Base permissions for conversation-related operations."""
    pass


class MessagePermissions(IsParticipantOfConversation):
    """Permissions for message operations."""
    pass


class ReadOnlyOrOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Others can only read.
    """

    def has_permission(self, request, view):
        """Check if user is authenticated."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Read permissions for participants, write permissions for owners."""
        # Read permissions for any participant
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'conversation'):
                return obj.conversation.participants.filter(id=request.user.id).exists()
            if hasattr(obj, 'participants'):
                return obj.participants.filter(id=request.user.id).exists()
        
        # Write permissions only for the owner
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        
        return False