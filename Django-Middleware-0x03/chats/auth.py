from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """POST username and password -> access and refresh JWTs."""


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """Create an account and return JWTs so the client is signed in straight away."""
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    return Response(
        {'user': UserSerializer(user).data, 'refresh': str(refresh), 'access': str(refresh.access_token)},
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET', 'PATCH'])
def user_profile(request):
    """View or update the signed-in user's profile."""
    if request.method == 'PATCH':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    return Response(UserSerializer(request.user).data)
