from post.models import Post
from profiles.models import User
from django.test import TestCase

class TestModels(TestCase):
    def test_post(self):
        user = User.objects.create_user(username='user', email='user@gmail.com' ,password='userpassword')
        post = Post.objects.create(description='description',owner_of_post=user)
        self.assertEqual(str(post), 'description')
        