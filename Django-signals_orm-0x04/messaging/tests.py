from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APITestCase

from .models import Message, MessageHistory, Notification

User = get_user_model()


class SignalTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='pass12345')
        self.bob = User.objects.create_user(username='bob', password='pass12345')

    def test_new_message_creates_notification(self):
        message = Message.objects.create(sender=self.alice, receiver=self.bob, content='Hello!')
        notification = Notification.objects.get()
        self.assertEqual((notification.user, notification.message), (self.bob, message))
        self.assertFalse(notification.is_read)

    def test_editing_message_logs_history(self):
        message = Message.objects.create(sender=self.alice, receiver=self.bob, content='Helo')
        message.content = 'Hello'
        message.edited_by = self.alice
        message.save()
        message.refresh_from_db()
        self.assertTrue(message.edited)
        self.assertIsNotNone(message.edited_at)
        history = MessageHistory.objects.get()
        self.assertEqual((history.old_content, history.edited_by), ('Helo', self.alice))
        # Saving without changing the content doesn't add history, and the update notifies nobody new
        message.save()
        self.assertEqual(MessageHistory.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)

    def test_deleting_user_removes_their_data(self):
        Message.objects.create(sender=self.alice, receiver=self.bob, content='Hi')
        Message.objects.create(sender=self.bob, receiver=self.alice, content='Hey')
        self.alice.delete()
        self.assertFalse(Message.objects.exists())
        self.assertFalse(Notification.objects.exists())

    def test_unread_manager(self):
        Message.objects.create(sender=self.alice, receiver=self.bob, content='one')
        Message.objects.create(sender=self.alice, receiver=self.bob, content='two', read=True)
        Message.objects.create(sender=self.bob, receiver=self.alice, content='three')
        self.assertEqual([m.content for m in Message.unread.unread_for_user(self.bob)], ['one'])


class ApiTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.alice = User.objects.create_user(username='alice', password='pass12345')
        self.bob = User.objects.create_user(username='bob', password='pass12345')
        self.client.force_authenticate(self.alice)

    def test_threaded_conversation(self):
        root = self.client.post('/api/thread/', {'receiver': self.bob.id, 'content': 'Root'}).data
        reply = Message.objects.create(sender=self.bob, receiver=self.alice, content='Reply', parent_message_id=root['id'])
        Message.objects.create(sender=self.alice, receiver=self.bob, content='Reply to reply', parent_message=reply)

        thread = self.client.get('/api/thread/').data
        self.assertEqual(len(thread), 1)
        self.assertEqual(thread[0]['replies'][0]['content'], 'Reply')
        self.assertEqual(thread[0]['replies'][0]['replies'][0]['content'], 'Reply to reply')

    def test_edit_and_history(self):
        message = Message.objects.create(sender=self.alice, receiver=self.bob, content='v1')
        self.assertTrue(self.client.patch(f'/api/messages/{message.id}/', {'content': 'v2'}).data['edited'])
        history = self.client.get(f'/api/messages/{message.id}/').data
        self.assertEqual(history[0]['old_content'], 'v1')
        # Bob can't edit Alice's message
        self.client.force_authenticate(self.bob)
        self.assertEqual(self.client.patch(f'/api/messages/{message.id}/', {'content': 'x'}).status_code, 404)

    def test_unread_endpoint(self):
        Message.objects.create(sender=self.bob, receiver=self.alice, content='unread')
        self.assertEqual(self.client.get('/api/messages/unread/').data[0]['content'], 'unread')

    def test_conversation_is_cached(self):
        Message.objects.create(sender=self.bob, receiver=self.alice, content='first')
        url = f'/api/conversations/{self.bob.id}/'
        self.assertEqual(len(self.client.get(url).data), 1)
        Message.objects.create(sender=self.bob, receiver=self.alice, content='second')
        self.assertEqual(len(self.client.get(url).data), 1)  # served from the cache
        cache.clear()
        self.assertEqual(len(self.client.get(url).data), 2)

    def test_delete_account(self):
        self.assertEqual(self.client.delete('/api/users/delete/').status_code, 204)
        self.assertFalse(User.objects.filter(username='alice').exists())
