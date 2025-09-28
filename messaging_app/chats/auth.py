"""
Authentication utilities for the messaging app.
"""
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer to include user information."""
    
    @classmethod
    def get_token(cls, user):
        """Add custom claims to token."""
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['user_id'] = user.id
        
        return token

    def validate(self, attrs):
        """Validate and return token data."""
        data = super().validate(attrs)
        
        # Add extra user information to response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }
        
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view."""
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer."""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 
                 'first_name', 'last_name']

    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def create(self, validated_data):
        """Create new user."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = CustomTokenObtainPairSerializer.get_token(user)
        access = refresh.access_token
        
        return Response({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(access),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_profile(request):
    """Get current user profile."""
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    })