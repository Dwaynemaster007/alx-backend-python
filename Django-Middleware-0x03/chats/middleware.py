"""Custom middleware for the messaging API.

Order in settings.MIDDLEWARE matters: all of these run after Django's
AuthenticationMiddleware so that ``request.user`` is available.
"""
import logging
import time
from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseForbidden, JsonResponse

logger = logging.getLogger('chats.requests')


class RequestLoggingMiddleware:
    """Log every request as ``<timestamp> - User: <user> - Path: <path>``."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        name = user if user is not None and user.is_authenticated else 'AnonymousUser'
        logger.info('%s - User: %s - Path: %s', datetime.now(), name, request.path)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """Block the API outside the hours set by CHAT_OPEN_HOUR and CHAT_CLOSE_HOUR (default 9 AM to 6 PM)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            open_hour = getattr(settings, 'CHAT_OPEN_HOUR', 9)
            close_hour = getattr(settings, 'CHAT_CLOSE_HOUR', 18)
            if not open_hour <= datetime.now().hour < close_hour:
                return HttpResponseForbidden(
                    f'Access is restricted to between {open_hour}:00 and {close_hour}:00.'
                )
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """Rate limit: each IP address may send CHAT_RATE_LIMIT messages (default 5) per CHAT_RATE_PERIOD seconds (default 60)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and 'messages' in request.path:
            limit = getattr(settings, 'CHAT_RATE_LIMIT', 5)
            period = getattr(settings, 'CHAT_RATE_PERIOD', 60)
            ip_address = self.get_client_ip(request)
            if not ip_address:
                return JsonResponse({'error': 'Could not identify client IP.'}, status=400)

            cache_key = f'rate_limit_{ip_address}'
            now = time.time()
            recent = [ts for ts in cache.get(cache_key, []) if now - ts < period]
            if len(recent) >= limit:
                return JsonResponse({'error': 'Message limit exceeded. Please try again later.'}, status=429)
            recent.append(now)
            cache.set(cache_key, recent, period)
        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


class RolepermissionMiddleware:
    """Only admins and moderators may open the Django admin site."""

    allowed_roles = {'ADMIN', 'MODERATOR'}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # The login page itself has to stay reachable
        if request.path.startswith('/admin/') and not request.path.startswith('/admin/login'):
            user = request.user
            if user.is_authenticated and not user.is_superuser:
                if (getattr(user, 'role', '') or '').upper() not in self.allowed_roles:
                    return HttpResponseForbidden('Access denied: admin or moderator privileges required.')
        return self.get_response(request)
