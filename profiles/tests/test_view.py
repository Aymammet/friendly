import os
from iface.settings import BASE_DIR

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse 
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.utils import timezone
from profiles.views import ProfileEditView, ProfileView
from profiles.models import User
from post.models import Post
from notifications.models import Notification

MEDIA_ROOT = os.path.join(BASE_DIR, 'profiles/tests')


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="aykos@gmail.com",
            username="aykos",
            password="passwordpassword"
        )
        self.user_2 = User.objects.create_user(
            email="aykos2@gmail.com",
            username="aykos2",
            password="passwordpassword2"
        )
        self.page_url = reverse('profiles:profile', args=[self.user.pk])
        self.post = Post.objects.create(description='Some description', owner_of_post=self.user)
        self.client.login(username='aykos', password='passwordpassword')
        # return super().setUp(self)

    def test_create_profile_page_url(self):
        response = self.client.get(self.page_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='profile.html')
        self.assertEqual(response.resolver_match.func.__name__, ProfileView.as_view().__name__)

    def test_edit_profile_page_url(self):
        page_url = reverse('profiles:edit_profile', args=[self.user.pk])
        response = self.client.get(page_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='profile_edit.html')
        self.assertEqual(response.resolver_match.func.__name__, ProfileEditView.as_view().__name__)
        
    
    def test_profiles_posts(self):
        page_url = reverse('profiles:edit_profile', args=[self.user.pk])
        post_2 = Post.objects.create(description='Some description2', owner_of_post=self.user_2)
        posts_2 = Post.objects.filter(owner_of_post=self.user)
        posts = Post.objects.all()
        self.assertEquals(posts_2.count(), 1)
        self.assertEquals(posts.count(), 2)
    

    def test_all_friends(self):
        friends = self.user.friends.all()
        self.assertEquals(friends.count(), 0)
        self.user.friends.add(self.user_2)
        self.assertEquals(friends.count(), 1)
        

    def test_send_friend_request(self):
        friends = self.user.friends.all()
        self.assertEquals(friends.count(), 0)
        notification_before = Notification.objects.all()
        self.assertEquals(notification_before.count(), 0)
        notification = Notification.objects.create(
            notification_type = 3,
            sender = self.user,
            receiver = self.user_2
        )
        notification_after = Notification.objects.all()
        self.assertEquals(notification_after.count(), 1)

    
    def test_accept_friend_request(self):
        friends = self.user.friends.all()
        self.assertEquals(friends.count(), 0)
        self.user.friends.add(self.user_2)
        self.assertEquals(friends.count(), 1)
        
    
    def test_cancel_friend_request(self):
        friends = self.user.friends.all()
        self.assertEquals(friends.count(), 0)
        notification_before = Notification.objects.all()
        self.assertEquals(notification_before.count(), 0)
        notification = Notification.objects.create(
            notification_type = 3,
            sender = self.user,
            receiver = self.user_2
        )
        notification_after_send_req = Notification.objects.all()
        self.assertEquals(notification_after_send_req.count(), 1)
        notification_del = Notification.objects.filter(
            notification_type = 3,
            sender = self.user,
            receiver = self.user_2
        )
        notification_del.delete()
        notification_after_del = Notification.objects.all()
        self.assertEquals(notification_after_del.count(), 0)
        self.assertEquals(friends.count(), 0)
        
    def test_remove_friend_(self):
        friends = self.user.friends.all()
        self.assertEquals(friends.count(), 0)
        self.user.friends.add(self.user_2)
        self.assertEquals(friends.count(), 1)
        selected_user = self.user.friends.get(pk=self.user_2.pk)
        selected_user.delete()
        self.assertEquals(friends.count(), 0)

    def test_user_search(self):
        response = self.client.get('/profiles/search', {'query':self.user})
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['profile_list'][0], self.user)
    
    def test_user_search_with_invalid_url(self):
        response = self.client.get('/profilesabcxyz/search', {'query':self.user_2})
        self.assertEqual(response.status_code, 404)