from rest_framework import serializers

from .models import Message, MessageHistory


class MessageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = ['id', 'old_content', 'edited_at', 'edited_by']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    receiver_username = serializers.StringRelatedField(source='receiver', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'receiver', 'receiver_username', 'content', 'timestamp',
            'edited', 'edited_at', 'read', 'parent_message',
        ]
        read_only_fields = ['edited', 'edited_at', 'read']


class ThreadSerializer(MessageSerializer):
    """A message with all of its replies nested underneath."""

    replies = serializers.SerializerMethodField()

    class Meta(MessageSerializer.Meta):
        fields = MessageSerializer.Meta.fields + ['replies']

    def get_replies(self, obj):
        return ThreadSerializer(obj.replies.all(), many=True).data
