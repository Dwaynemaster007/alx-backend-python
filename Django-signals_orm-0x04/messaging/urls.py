from django.urls import path

from .views import (
    CachedConversationView, MessageEditView, ThreadedConversationView, UnreadMessagesView,
    cached_message_list_view, delete_user,
)

urlpatterns = [
    path('users/delete/', delete_user, name='delete-user'),
    path('thread/', ThreadedConversationView.as_view(), name='threaded-conversation'),
    path('messages/<int:pk>/', MessageEditView.as_view(), name='message-edit'),
    path('messages/unread/', UnreadMessagesView.as_view(), name='unread-messages'),
    path('messages/cached/', cached_message_list_view, name='cached-message-list'),
    path('conversations/<int:user_id>/', CachedConversationView.as_view(), name='cached-conversation'),
]
