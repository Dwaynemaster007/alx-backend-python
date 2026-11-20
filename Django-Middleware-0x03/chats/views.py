from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from .models import Conversation, Message
from .filters import MessageFilter
from .permissions import IsParticipantOfConversation
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer

User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    """Conversations the signed-in user takes part in. POST participant_ids to start one."""

    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        return (
            Conversation.objects.filter(participants=self.request.user)
            .prefetch_related('participants', 'messages__sender')
            .order_by('-created_at')
            .distinct()
        )


class MessageViewSet(viewsets.ModelViewSet):
    """Messages in the user's conversations.

    Nested: /api/conversations/<conversation_pk>/messages/
    Flat:   /api/messages/?conversation=<id>
    """

    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['message_body']
    ordering = ['sent_at']

    def get_queryset(self):
        queryset = Message.objects.filter(conversation__participants=self.request.user).select_related('sender')
        conversation_id = self.kwargs.get('conversation_pk') or self.request.query_params.get('conversation')
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        return queryset.distinct()

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk') or self.request.data.get('conversation')
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        if not conversation.participants.filter(pk=self.request.user.pk).exists():
            raise PermissionDenied('You are not a participant in this conversation.')
        serializer.save(sender=self.request.user, conversation=conversation)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Browse users (e.g. to pick conversation participants)."""

    queryset = User.objects.order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
