from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Room(models.Model):
    room_id = models.IntegerField(primary_key=True)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(max_length=10000)
    time_of_message = models.TimeField(default = timezone.now)