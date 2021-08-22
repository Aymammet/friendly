from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse, resolve
from .views import CustomLoginView, CustomRegisterView
from django.contrib.auth.views import LogoutView
from profiles.models import User
import json


class URLTests(TestCase):
    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_url_is_resolved(self):
       url = reverse('authenticate:main_page')
       self.assertEquals(resolve(url).func.view_class, CustomLoginView)
       

    def test_logout_url_is_resolved(self):
        url = reverse('authenticate:logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)


class ViewTests(TestCase):
    def test_CustomLoginView_GET(self):
        client = Client()
        response = client.get(reverse('authenticate:main_page'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_page.html')

    def test_CustomRegisterView_GET(self):
        client = Client()
        response = client.get(reverse('authenticate:register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')


class RegisterTests(TestCase):
    def setUp(self) -> None:
        self.username = 'testuser'
        self.email = 'testuser@gmail.com'
        self.password = 'friendlyproject2021'

    def test_register_page_url(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='register.html')

    def test_register_page_view_name(self):
        response = self.client.get(reverse('authenticate:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='register.html')

    def test_register_form(self):
        response = self.client.post(reverse('authenticate:register'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 200)

        users = User.objects.all()
        self.assertEqual(users.count(), 1)


class AdminTest(LiveServerTestCase):

    def setUp(self):
        self.client = Client()

    def test_login(self):
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 302)

        self.client.login(username='XXX', password="XXX")
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 302)

    def test_logout(self):
        self.client.login(username='XXX', password="XXX")
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 302)

        self.client.logout()
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 302)

       