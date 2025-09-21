from rest_framework import viewsets
from .models import User, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        # Filter messages to only show those in conversations the user is a part of
        user_conversations = self.request.user.conversations.all()
        return Message.objects.filter(conversation__in=user_conversations).order_by('sent_at')

    def perform_create(self, serializer):
        # Automatically set the sender to the current authenticated user
        serializer.save(sender=self.request.user)