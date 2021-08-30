from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse, resolve
from authenticate.views import CustomLoginView, CustomRegisterView
from django.contrib.auth.views import LogoutView
from profiles.models import User
from authenticate.form import LoginForm
from django.contrib.messages import get_messages


class TestLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@gmail.com' ,password='userpassword')
        self.client = Client()
        # self.client.force_login(self.user)
        self.login_page_url = reverse('authenticate:main_page')

    def test_CustomLoginView_GET(self):
        response = self.client.get(self.login_page_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_page.html')
        self.assertEqual(response.resolver_match.func.__name__, CustomLoginView.as_view().__name__)
    
    def test_valid_form(self):
        response = self.client.post(self.login_page_url, data={
            'username': 'user',
            'password': 'userpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.is_authenticated, True)

    def test_form_with_no_password(self):
        form_data = {'username': 'user', 'password': '' }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_no_username(self):
        form_data = {'username': '', 'password': 'userpassword' }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form['username'].errors, ['This field is required.'])

    def test_form_with_unregistered_user(self):
        form_data = {'username': 'someone', 'password': 'something' }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        

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
        self.assertEqual(response.resolver_match.func.__name__, CustomRegisterView.as_view().__name__)
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

    def test_register_form_wrong_password(self):
        response = self.client.post(reverse('authenticate:register'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': 'anotherpassowrd'
        })
        self.assertEqual(response.status_code, 200)

        users = User.objects.all()
        self.assertEqual(users.count(), 0)

    def test_register_form_same_username(self):
        response = self.client.post(reverse('authenticate:register'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
        })
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post(reverse('authenticate:register'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
        })
        self.assertEqual(response2.status_code, 200)
        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_register_form_same_email(self):
        response = self.client.post(reverse('authenticate:register'), data={
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password,
        })
        self.assertEqual(response.status_code, 200)

        response2 = self.client.post(reverse('authenticate:register'), data={
            'username': 'username2',
            'email': self.email,
            'password1': 'passwordpassword',
            'password2': 'passwordpassword',
        })
        self.assertEqual(response2.status_code, 200)

        users = User.objects.all()
        # self.assertEqual(users.count(), 1)

        # 0 left