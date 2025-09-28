"""
Filter classes for the messaging app.
"""
import django_filters
from django.contrib.auth.models import User
from .models import Message, Conversation


class MessageFilter(django_filters.FilterSet):
    """Filter class for messages."""
    
    # Filter by conversation
    conversation = django_filters.ModelChoiceFilter(
        queryset=Conversation.objects.all(),
        field_name='conversation'
    )
    
    # Filter by sender
    sender = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='sender'
    )
    
    # Filter by date range
    created_after = django_filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='lte'
    )
    
    # Filter by date (specific day)
    created_date = django_filters.DateFilter(
        field_name='created_at', 
        lookup_expr='date'
    )
    
    # Search in message content
    content = django_filters.CharFilter(
        field_name='content', 
        lookup_expr='icontains'
    )
    
    # Filter messages from a specific user (by username)
    sender_username = django_filters.CharFilter(
        field_name='sender__username', 
        lookup_expr='iexact'
    )

    class Meta:
        model = Message
        fields = {
            'created_at': ['exact', 'gte', 'lte', 'date'],
            'content': ['icontains', 'exact'],
            'conversation': ['exact'],
            'sender': ['exact'],
        }


class ConversationFilter(django_filters.FilterSet):
    """Filter class for conversations."""
    
    # Filter conversations with specific participants
    participant = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='participants'
    )
    
    # Filter by participant username
    participant_username = django_filters.CharFilter(
        field_name='participants__username',
        lookup_expr='icontains'
    )
    
    # Filter by creation date
    created_after = django_filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at', 
        lookup_expr='lte'
    )
    
    # Filter conversations that have recent activity
    has_recent_messages = django_filters.BooleanFilter(
        method='filter_recent_messages'
    )
    
    def filter_recent_messages(self, queryset, name, value):
        """Filter conversations with recent messages (last 24 hours)."""
        if value:
            from django.utils import timezone
            from datetime import timedelta
            
            recent_time = timezone.now() - timedelta(days=1)
            return queryset.filter(messages__created_at__gte=recent_time).distinct()
        return queryset

    class Meta:
        model = Conversation
        fields = {
            'created_at': ['exact', 'gte', 'lte'],
            'participants': ['exact'],
        }


class UserMessageFilter(django_filters.FilterSet):
    """Filter messages for specific user interactions."""
    
    # Filter messages between two specific users
    with_user = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        method='filter_with_user'
    )
    
    # Filter messages by time range
    time_range = django_filters.ChoiceFilter(
        choices=[
            ('hour', 'Last Hour'),
            ('day', 'Last Day'),
            ('week', 'Last Week'),
            ('month', 'Last Month'),
        ],
        method='filter_by_time_range'
    )

    def filter_with_user(self, queryset, name, value):
        """Filter messages in conversations with a specific user."""
        if value:
            # Get conversations where both current user and specified user participate
            conversations = Conversation.objects.filter(
                participants=self.request.user
            ).filter(participants=value)
            
            return queryset.filter(conversation__in=conversations)
        return queryset

    def filter_by_time_range(self, queryset, name, value):
        """Filter messages by time range."""
        if value:
            from django.utils import timezone
            from datetime import timedelta
            
            time_deltas = {
                'hour': timedelta(hours=1),
                'day': timedelta(days=1),
                'week': timedelta(weeks=1),
                'month': timedelta(days=30),
            }
            
            if value in time_deltas:
                time_threshold = timezone.now() - time_deltas[value]
                return queryset.filter(created_at__gte=time_threshold)
        
        return queryset

    class Meta:
        model = Message
        fields = ['with_user', 'time_range']