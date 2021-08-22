from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
import datetime


class Post(models.Model):
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to = 'images/')
    created_date = models.DateTimeField(default=timezone.now)
    owner_of_post = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_by", blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="disliked_by", blank=True)
   
    def __str__(self):
        return self.description
    

class Comments(models.Model):     
     post = models.ForeignKey(Post, on_delete=models.CASCADE)
     owner_of_comments = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
     comment = models.CharField(max_length=1000)
     created_date = models.DateTimeField(default=timezone.now)

     def __str__(self):
        return self.comment

    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE )



