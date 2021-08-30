from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from profiles.models import User
from django.contrib.auth.forms import AuthenticationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)
    class Meta:
        fields = ['remember_me']
