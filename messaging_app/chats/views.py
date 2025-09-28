"""
Views for the messaging app with authentication and permissions.
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from .permissions import (
    IsParticipantOfConversation, 
    IsOwnerOrParticipant, 
    IsMessageOwner,
    ReadOnlyOrOwner
)
from .pagination import MessagePagination, ConversationPagination
from .filters import MessageFilter, ConversationFilter, UserMessageFilter


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing conversations."""
    
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = ConversationPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ConversationFilter
    search_fields = ['participants__username', 'participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']

    def get_queryset(self):
        """Return conversations where user is a participant."""
        return Conversation.objects.filter(
            participants=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        """Add current user as participant when creating conversation."""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages in a conversation."""
        conversation = self.get_object()
        messages = Message.objects.filter(conversation=conversation).order_by('-created_at')
        
        # Apply pagination
        paginator = MessagePagination()
        page = paginator.paginate_queryset(messages, request)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """Add a participant to the conversation."""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            conversation.participants.add(user)
            return Response({'message': 'Participant added successfully'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def remove_participant(self, request, pk=None):
        """Remove a participant from the conversation."""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            conversation.participants.remove(user)
            return Response({'message': 'Participant removed successfully'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing messages."""
    
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return messages from conversations where user is a participant."""
        user_conversations = Conversation.objects.filter(participants=self.request.user)
        return Message.objects.filter(conversation__in=user_conversations)

    def get_permissions(self):
        """Set different permissions for different actions."""
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsMessageOwner]
        else:
            permission_classes = [IsParticipantOfConversation]
        
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Set sender as current user when creating message."""
        serializer.save(sender=self.request.user)

    @action(detail=False, methods=['get'])
    def my_messages(self, request):
        """Get all messages sent by the current user."""
        messages = Message.objects.filter(sender=request.user).order_by('-created_at')
        
        # Apply filtering
        filterset = UserMessageFilter(request.GET, queryset=messages, request=request)
        if filterset.is_valid():
            messages = filterset.qs
        
        # Apply pagination
        paginator = MessagePagination()
        page = paginator.paginate_queryset(messages, request)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def conversation_messages(self, request):
        """Get messages from a specific conversation."""
        conversation_id = request.query_params.get('conversation_id')
        
        if not conversation_id:
            return Response(
                {'error': 'conversation_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            # Check if user is participant
            if not conversation.participants.filter(id=request.user.id).exists():
                return Response(
                    {'error': 'You are not a participant in this conversation'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            messages = Message.objects.filter(conversation=conversation).order_by('-created_at')
            
            # Apply pagination
            paginator = MessagePagination()
            page = paginator.paginate_queryset(messages, request)
            if page is not None:
                serializer = MessageSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
            
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
            
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user management (read-only)."""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'first_name', 'last_name']
    ordering = ['username']

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)