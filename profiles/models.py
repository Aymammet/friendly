from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.templatetags.static import static
from django.conf import settings


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


   












