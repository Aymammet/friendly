from django.db import models
from django.conf import settings
from django.utils import timezone
from post.models import Post, Comments
from dm.models import Room


class Notification(models.Model):
        notification_type = models.IntegerField()
        receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notif_to', null=True)
        sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notif_from', null=True)
        post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
        comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
        room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='+', blank=True, null=True) 
        date = models.DateTimeField(default=timezone.now)
        not_text = models.CharField(max_length=500, blank=True, null=True)
        user_has_seen = models.BooleanField(default=False)

        # 1 - like, 2-Comment, 3-Follow,  4-Direct Message
      

        def remove_notification(self):
                self.delete()
            
