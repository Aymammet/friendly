from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.forms.fields import DateTimeField
import datetime 
from .models import Post, Comments



class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
