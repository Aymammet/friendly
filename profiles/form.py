from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
import datetime 
from .models import User
from django.forms.fields import DateField, DateTimeField


class DateInput(forms.DateInput):
    input_type = 'date'


class UpdateProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'image', 'birth_date', 'bio', ]
        widgets={
            'birth_date': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date'})
            }


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=30)


class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000)