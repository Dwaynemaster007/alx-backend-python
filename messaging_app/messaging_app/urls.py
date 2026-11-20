"""URL configuration for the messaging_app project."""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from chats.auth import CustomTokenObtainPairView, register_user, user_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentication
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', register_user, name='register'),
    path('api/auth/profile/', user_profile, name='user_profile'),
    # Conversations, messages and users
    path('api/', include('chats.urls')),
    # DRF browsable API login (development)
    path('api-auth/', include('rest_framework.urls')),
]
