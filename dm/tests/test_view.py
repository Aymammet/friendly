from django.test import TestCase, Client
from django.urls import reverse
from dm.models import Room, Message
from profiles.models import User
from dm.views import Inbox, JsonMessages, JsonMessages_get
import json

class TestInboxView(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', email='user@gmail.com' ,password='userpassword')
        self.client = Client()
        self.client.force_login(self.user)
        self.login_page_url = reverse('dm:inbox')

    def test_InboxView_GET(self):
        response = self.client.get(self.login_page_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox.html')
        self.assertEqual(response.resolver_match.func.__name__, Inbox.as_view().__name__)
        self.assertEqual(self.user.friends.count(), 0)
        
    def test_InboxView_GET_with_friends(self):
        user_one = User.objects.create(username='user_one', email='user_one@gmail.com' ,password='userpassword_one')
        user_two = User.objects.create(username='user_two', email='user_two@gmail.com' ,password='userpassword_two')
        user_three = User.objects.create(username='user_three', email='user_three@gmail.com' ,password='userpassword_three')
        self.user.friends.add(user_one)
        self.user.friends.add(user_two)
        self.user.friends.add(user_three)
        self.assertEqual(self.user.friends.count(), 3)
        self.assertEqual(self.user.get_room_id(user_one), 102)
    
    
# class JsonViewTestCase(TestCase):
#     def test_json_view(self):
#         response = self.client.post(
#             reverse('dm:messages', args=('message', 'This is new message from html', 'friend')),
#             json.dumps({'user': 'me@example.com',}),
#             'json',
#             HTTP_X_REQUESTED_WITH='XMLHttpRequest',
#         )
#         json_string = response.content
#         response_data = json.loads(json_string)
        # do smth.