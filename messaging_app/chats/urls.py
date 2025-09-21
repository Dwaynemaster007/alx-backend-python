# chats/urls.py
from rest_framework_nested import routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet

# Create the main router
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create a nested router for messages within conversations
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Combine the URLs
urlpatterns = router.urls + conversations_router.urls