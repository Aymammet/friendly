from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Room, Message
from profiles.models import User
from notifications.models import Notification
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

class Inbox(View):
    def get(self, request, *args, **kwargs):
        user  = self.request.user
        context = {
            'friends' : user.friends.all() 
            }
        # kwargs.get('friend').exists():
        return render(request, 'inbox.html', context)


def create_room(user1_id, user2_id):
    users = sorted([user1_id, user2_id])
    return int('0'.join([str(users[0]), str(users[1])]))


class JsonMessages(View):
    def post(self, request):
        body = json.loads(request.body)
        friend = get_object_or_404(User, username=body['friend'])
        new_message = body['message']
        room_id = create_room(friend.pk, request.user.pk)
        room = get_object_or_404(Room, room_id=room_id)
        message = Message.objects.filter(room=room)
        if new_message != '':
            Message.objects.filter(room=room).create(message=new_message, room=room, user=self.request.user)
            notification = Notification.objects.create(
            notification_type=4,
            sender = request.user,
            receiver = friend,
            room = room
            )
        return JsonResponse({'messages':list(message.values())})


class JsonMessages_get(View):
    def post(self, request):
        body = json.loads(request.body)
        friend = get_object_or_404(User, username=body['friend'])
        if friend.image:
            im = friend.image.url
        else:
            im = '../../static/images/default_image.jpg'
        room_id = create_room(friend.pk, request.user.pk)
        room = get_object_or_404(Room, room_id=room_id)
        message = Message.objects.filter(room=room)
        return JsonResponse({'messages':list(message.values()), 'image':im, 'username':friend.username, 'name':friend.name, 'surname':friend.surname})