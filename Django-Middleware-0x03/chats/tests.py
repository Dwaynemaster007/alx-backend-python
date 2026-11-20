from datetime import datetime
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


@override_settings(CHAT_OPEN_HOUR=0, CHAT_CLOSE_HOUR=24, CHAT_RATE_LIMIT=100)
class MessagingApiTests(APITestCase):
    def register(self, username):
        response = self.client.post('/api/auth/register/', {
            'username': username, 'email': f'{username}@example.com', 'password': 'Str0ng-pass!',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        return response.data

    def use(self, account):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {account['access']}")

    def test_user_model_defaults(self):
        user = User.objects.create_user(username='guest', password='Str0ng-pass!')
        self.assertEqual(user.role, User.Role.GUEST)

    def test_requires_authentication(self):
        self.assertEqual(self.client.get('/api/conversations/').status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_returns_tokens(self):
        self.register('alice')
        response = self.client.post('/api/auth/login/', {'username': 'alice', 'password': 'Str0ng-pass!'}, format='json')
        self.assertIn('access', response.data)

    def test_conversation_and_messages(self):
        alice, bob, eve = self.register('alice'), self.register('bob'), self.register('eve')

        self.use(alice)
        convo = self.client.post('/api/conversations/', {'participant_ids': [bob['user']['id']]}, format='json')
        self.assertEqual(convo.status_code, status.HTTP_201_CREATED, convo.data)
        convo_id = convo.data['id']

        sent = self.client.post(f'/api/conversations/{convo_id}/messages/', {'message_body': 'Hi Bob!'}, format='json')
        self.assertEqual(sent.status_code, status.HTTP_201_CREATED, sent.data)
        message_id = sent.data['id']

        # Bob can read the conversation and reply
        self.use(bob)
        self.assertEqual(len(self.client.get('/api/conversations/').data['results']), 1)
        reply = self.client.post(f'/api/conversations/{convo_id}/messages/', {'message_body': 'Hey Alice'}, format='json')
        self.assertEqual(reply.status_code, status.HTTP_201_CREATED)
        messages = self.client.get(f'/api/conversations/{convo_id}/messages/').data['results']
        self.assertEqual([m['message_body'] for m in messages], ['Hi Bob!', 'Hey Alice'])

        # Bob can't edit Alice's message
        response = self.client.patch(f'/api/messages/{message_id}/', {'message_body': 'edited'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Eve isn't a participant: she sees nothing and can't post
        self.use(eve)
        self.assertEqual(len(self.client.get('/api/conversations/').data['results']), 0)
        response = self.client.post(f'/api/conversations/{convo_id}/messages/', {'message_body': 'Hello?'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_update(self):
        account = self.register('carol')
        self.use(account)
        response = self.client.patch('/api/auth/profile/', {'phone_number': '+26876000000'}, format='json')
        self.assertEqual(response.data['phone_number'], '+26876000000')


class MiddlewareTests(APITestCase):
    def setUp(self):
        cache.clear()

    def fake_now(self, hour):
        return mock.patch('chats.middleware.datetime', wraps=datetime,
                          **{'now.return_value': datetime(2026, 1, 5, hour, 0)})

    def test_api_closed_outside_hours(self):
        with self.fake_now(20):
            self.assertEqual(self.client.get('/api/conversations/').status_code, status.HTTP_403_FORBIDDEN)
        with self.fake_now(10):
            self.assertEqual(self.client.get('/api/conversations/').status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(CHAT_OPEN_HOUR=0, CHAT_CLOSE_HOUR=24, CHAT_RATE_LIMIT=2)
    def test_message_rate_limit(self):
        codes = [self.client.post('/api/messages/', {}, format='json').status_code for _ in range(3)]
        self.assertNotEqual(codes[1], 429)
        self.assertEqual(codes[2], 429)

    def test_admin_requires_admin_role(self):
        guest = User.objects.create_user(username='guest', password='Str0ng-pass!', is_staff=True)
        self.client.force_login(guest)
        self.assertEqual(self.client.get('/admin/').status_code, status.HTTP_403_FORBIDDEN)

        guest.role = User.Role.ADMIN
        guest.save()
        self.assertEqual(self.client.get('/admin/').status_code, status.HTTP_200_OK)

    def test_requests_are_logged(self):
        with self.assertLogs('chats.requests', level='INFO') as logs:
            self.client.get('/admin/login/')
        self.assertIn('User: AnonymousUser - Path: /admin/login/', logs.output[0])
