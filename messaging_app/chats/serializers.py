# messaging_app/chats/serializers.py

from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'password']
        read_only_fields = ['user_id']

    def create(self, validated_data):
        # The password field is explicitly handled here to hash the password.
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password is not None:
            user.set_password(password)
            user.save()
        return user

class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.ReadOnlyField(source='sender.email')
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at', 'sender_email']
        read_only_fields = ['sender', 'sent_at', 'message_id']

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
        read_only_fields = ['conversation_id', 'created_at', 'messages']

    def get_participants(self, obj):
        return [user.email for user in obj.participants.all()]

    def validate(self, data):
        if len(data.get('participants', [])) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return data