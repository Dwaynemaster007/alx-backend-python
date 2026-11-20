from django.db import models


class UnreadMessagesQuerySet(models.QuerySet):
    def unread_for_user(self, user):
        """Messages sent to ``user`` that they haven't read yet."""
        return self.filter(receiver=user, read=False)


class UnreadMessagesManager(models.Manager):
    """Usage: ``Message.unread.unread_for_user(request.user)``."""

    def get_queryset(self):
        return UnreadMessagesQuerySet(self.model, using=self._db)

    def unread_for_user(self, user):
        return self.get_queryset().unread_for_user(user)
