from django.test import TestCase, Client
from django.urls import reverse
from profiles.models import User
from post.models import Post, Comments 
from notifications.models import Notification
from notifications.views import PostNotification, RemoveNotification, RemoveNotification2, RemoveNotification3 
import json
from django.utils.encoding import force_text

class TestPostNotification(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', email='user@gmail.com' ,password='userpassword')
        self.client = Client()
        self.client.force_login(self.user)

    def test_PostNotifications_GET(self):
        user_two = User.objects.create(username='user_two', email='user_two@gmail.com' ,password='userpassword_two')
        post_one = Post.objects.create(description='description', owner_of_post=self.user)
        notification_one = Notification.objects.create(notification_type=1, receiver=user_two, sender=self.user, post=post_one )
        notification_two = Notification.objects.create(notification_type=2, receiver=user_two, sender=self.user )
        notifications = Notification.objects.all()
        self.assertEqual(notifications.filter(notification_type=1).count(), 1)
        self.assertEqual(notifications.count(), 2)


class TestRemoveNotification(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', email='user@gmail.com' ,password='userpassword')
        self.client = Client()
        self.client.force_login(self.user)

    def test_RemoveNotifications_GET(self):
        user_two = User.objects.create(username='user_two', email='user_two@gmail.com' ,password='userpassword_two')
        post_one = Post.objects.create(description='description', owner_of_post=self.user)
        notification_one = Notification.objects.create(notification_type=1, receiver=user_two, sender=self.user, post=post_one )
        notification_two = Notification.objects.create(notification_type=2, receiver=user_two, sender=self.user )
        notifications = Notification.objects.all()
        self.assertEqual(notifications.filter(notification_type=1).count(), 1)
        self.assertEqual(notifications.count(), 2)
        notification_one.delete()
        self.assertEqual(notifications.count(), 1)
        nt = Notification.objects.get(pk=notification_two.pk)
        nt.delete()
        self.assertEqual(notifications.count(), 0)
        

class TestRemoveNotification2(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', email='user@gmail.com' ,password='userpassword')
        self.user_2 = User.objects.create(username='user2', email='user2@gmail.com' ,password='userpassword2')
        self.client = Client()
        self.client.force_login(self.user)
        self.post = Post.objects.create(description='some_description', owner_of_post=self.user)

   
   