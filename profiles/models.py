from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone
import datetime
# from django.db.models.signals import post_save
from django.conf import settings
from django.templatetags.static import static
from django.conf import settings
#from post import Post

#Profile
class User(AbstractUser):
    name = models.CharField(max_length=30, blank=True, null=True)
    surname = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField()
    image = models.ImageField(blank=True, null=True, upload_to = 'profile_images')
    bio = models.TextField(max_length=1000, blank=True, null=True)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name = 'my_friends')
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()    

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)
    

    def get_room_id(self, friend):
        users = sorted([self.pk, friend.pk])
        return int('0'.join([str(users[0]), str(users[1])]))

    
    def get_profile_image(self):
        if not self.image:
            return static('images/default_image.jpg')
        return self.image.url


class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+' )
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class MessageModel(models.Model):
    thread = models.ForeignKey('Thread', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+' )
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+' )
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='message_photos', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)



   












