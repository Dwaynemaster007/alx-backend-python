from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message
from .serializers import MessageHistorySerializer, MessageSerializer, ThreadSerializer

User = get_user_model()


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request):
    """Delete your own account. The post_delete signal cleans up related data."""
    request.user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class ThreadedConversationView(APIView):
    """GET: your top-level conversations with replies nested. POST: send a message or a reply."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = (
            Message.objects.filter(Q(sender=user) | Q(receiver=user), parent_message__isnull=True)
            .select_related('sender', 'receiver')
            .prefetch_related('replies__sender', 'replies__receiver', 'replies__replies')
        )
        return Response(ThreadSerializer(queryset, many=True).data)

    def post(self, request):
        receiver = get_object_or_404(User, pk=request.data.get('receiver'))
        if receiver == request.user:
            return Response({'error': "You can't message yourself."}, status=status.HTTP_400_BAD_REQUEST)
        parent = None
        if request.data.get('parent_message'):
            parent = get_object_or_404(
                Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)),
                pk=request.data['parent_message'],
            )
        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=request.data.get('content', ''),
            parent_message=parent,
        )
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class MessageEditView(APIView):
    """PATCH: edit one of your messages. GET: see its edit history."""

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        message = get_object_or_404(Message, pk=pk, sender=request.user)
        message.content = request.data.get('content', message.content)
        message.edited_by = request.user
        message.save()
        return Response(MessageSerializer(message).data)

    def get(self, request, pk):
        message = get_object_or_404(
            Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)), pk=pk
        )
        return Response(MessageHistorySerializer(message.history.all(), many=True).data)


class UnreadMessagesView(generics.ListAPIView):
    """Your unread messages, using the custom manager and fetching only the fields shown."""

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Message.unread.unread_for_user(self.request.user)
            .select_related('sender', 'receiver')
            .only('id', 'sender__username', 'receiver__username', 'content', 'timestamp',
                  'edited', 'edited_at', 'read', 'parent_message')
        )


@method_decorator(cache_page(60), name='dispatch')
class CachedConversationView(APIView):
    """The messages in one conversation between you and another user, cached for 60 seconds."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        messages = Message.objects.filter(
            Q(sender=request.user, receiver_id=user_id) | Q(sender_id=user_id, receiver=request.user)
        ).select_related('sender', 'receiver')
        return Response(MessageSerializer(messages, many=True).data)


@cache_page(60)
def cached_message_list_view(request):
    """All of your messages as plain JSON, cached for 60 seconds."""
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'Authentication required.'}, status=401)
    messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).values(
        'id', 'sender__username', 'receiver__username', 'content', 'timestamp'
    )
    return JsonResponse(list(messages), safe=False)
