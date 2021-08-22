from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.utils import timezone
# from profiles.models import User
from post.models import Post
from django.contrib.auth.models import User
# Create your tests here.




class ViewTests(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='aykos', 
            email='aykos@gmail.com',
            password='demamnahaykos'
            )
        self.client = Client()

    def test_createPost_form(self):
        user = User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.client.login(username='foo', password='bar')
        
        self.user = User.objects.create(
            username='aykos2', 
            email='aykos2@gmail.com',
            password='demamnahaykos'
            ).save()
        self.client.login(username="aykos",password="demamnahaykos")
        response = self.client.post(reverse('post:new_post'), data={
            'owner_of_post' : user,
            'description' : 'asasasa'
        })
        self.assertEqual(response.status_code, 200)

        post = Post.objects.all()
        self.assertEqual(post.count(), 1)