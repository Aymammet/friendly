import os

from django.contrib.staticfiles import testing
from iface.settings import BASE_DIR

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.utils import timezone
from profiles.models import User
from post.models import Post, Comments
from post.views import CustomLikeView, CustomDislikeView, CustomDeleteView

MEDIA_ROOT = os.path.join(BASE_DIR, 'post/tests')


class PostListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.page_url = reverse('post:home')
        self.user = User.objects.create_user(
            email="aykos@gmail.com",
            username="aykos",
            password="passwordpassword"
        )
        self.client.login(username='aykos', password='passwordpassword')
        # return super().setUp(self)

    def test_post_list(self):
        response = self.client.get(self.page_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        Post.objects.create(description='some description', owner_of_post=self.user)
        posts = Post.objects.all()
        self.assertEquals(posts.count(), 1)
        

class CreatePostView(TestCase):
    def setUp(self):
        self.client = Client()
        self.page_url = reverse('post:new_post')
        self.user = User.objects.create_user(
            email="aykos@gmail.com",
            username="aykos",
            password="passwordpassword"
        )
        self.client.login(username='aykos', password='passwordpassword')
        # return super().setUp(self)

    def test_create_post_page_url(self):
        response = self.client.get(self.page_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='new_post.html')

    def test_createPost(self):
        response = self.client.post(self.page_url, {'description': 'some description','owner_of_post': self.user})
        post = Post.objects.all()
        self.assertEqual(post.count(), 1)

    def test_createPost_with_no_image_no_description(self):
        response = self.client.post('/', {'owner_of_post': self.user})
        self.assertEquals(response.status_code, 200)
        post = Post.objects.all()
        self.assertEqual(post.count(), 0)


class PostUpdateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="aykos@gmail.com",
            username="aykos",
            password="passwordpassword"
        )
        self.client.login(username='aykos', password='passwordpassword')
        self.post = Post.objects.create(description='some description', owner_of_post=self.user)
        self.page_url = reverse('post:edit_post', args=[self.post.pk])
        # return super().setUp(self)

    def test_post_update(self):
        response = self.client.get(self.page_url)
        self.assertEquals(self.post.description, 'some description')
        self.post.description = 'another_description'
        self.assertNotEquals(self.post.description, 'some description')
        self.assertEquals(self.post.description, 'another_description')


class DeletePostView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="aykos@gmail.com",
            username="aykos",
            password="passwordpassword"
        )
        self.client.login(username='aykos', password='passwordpassword')
        self.post = Post.objects.create(description='some description', owner_of_post=self.user)
        self.page_url = reverse('post:delete_post', args=[self.post.pk])
        # return super().setUp(self)

    def test_delete_post_page_url(self):
        response = self.client.get(self.page_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='delete_post.html')
        self.assertEqual(response.resolver_match.func.__name__, CustomDeleteView.as_view().__name__)
    
    def test_delete_post(self):
        post = Post.objects.all()
        self.assertEquals(post.count(), 1)
        response = self.client.post(self.page_url)
        self.assertEquals(post.count(), 0)


class CommentView(TestCase):
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
        self.client.login(username='aykos', password='passwordpassword')
        self.post = Post.objects.create(description='some description', owner_of_post=self.user)
        self.page_url = reverse('post:home')
    
    def test_create_comment(self):
        response = self.client.post(reverse('post:comment'), {'post_pk':self.post.pk, 'comment':'This is a comment'}, content_type="application/json")
        comments = Comments.objects.all()
        self.assertEquals(comments.count(), 1)
        response = self.client.post(reverse('post:comment'), {'post_pk':self.post.pk, 'comment':'This is another comment'}, content_type="application/json")
        self.assertEquals(comments.count(), 2)
        

class LikeView(TestCase):
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
        self.client.login(username='aykos', password='passwordpassword')
        self.post = Post.objects.create(description='some description', owner_of_post=self.user)
        self.page_url = reverse('post:home')
    
    def test_like_post(self):
        response = self.client.post(reverse('post:post_like'), {'post_pk':self.post.pk}, content_type="application/json")
        self.assertEquals(response.resolver_match.func.__name__, CustomLikeView.as_view().__name__)
        self.assertEquals(self.post.likes.count(), 1)
        response = self.client.post(reverse('post:post_like'), {'post_pk':self.post.pk}, content_type="application/json")
        self.assertEquals(self.post.likes.count(), 0)
        
    
    def test_dislike_post(self):
        response = self.client.post(reverse('post:post_dislike'), {'disliked_post_pk':self.post.pk}, content_type="application/json")
        self.assertEquals(response.resolver_match.func.__name__, CustomDislikeView.as_view().__name__)
        self.assertEquals(self.post.dislikes.count(), 1)
        response = self.client.post(reverse('post:post_dislike'), {'disliked_post_pk':self.post.pk}, content_type="application/json")
        self.assertEquals(self.post.dislikes.count(), 0)
        
    