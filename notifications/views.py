from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView, CreateView, ListView, DetailView, DeleteView, UpdateView, View
from .models import Notification
from post.models import Post
from profiles.models import User
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.edit import FormMixin
from django.db.models import Q
import json

class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)
        notification.remove_notification()
        return redirect('post:post_detail', pk=post.pk)


class RemoveNotification(View):
    def post(self, request):
        body = json.loads(request.body)
        notification = Notification.objects.get(pk=body['notf_pk'])
        notification.remove_notification()
        user = request.user
        notification_count = Notification.objects.filter(receiver=user).count()
        notification_count2 = Notification.objects.filter(receiver=user).filter(notification_type=4).count()
        total = notification_count - notification_count2
        all_notf = Notification.objects.filter(receiver=user).values()
        for notf in all_notf:
            notf['sender_name'] = User.objects.get(pk=notf['sender_id']).username
        return JsonResponse({'notification_count': total, 'all_notfs':list(all_notf)})


class RemoveNotification2(View):
    def post(self, request):
        user = request.user
        notification_count = Notification.objects.filter(receiver=user).count()
        notification_count2 = Notification.objects.filter(receiver=user).filter(notification_type=4).count()
        total = notification_count - notification_count2
        return JsonResponse({'notification_count': total, 'notification_count_m':notification_count2 })


class RemoveNotification3(View):
    def post(self, request):
        user = request.user
        notification_count = Notification.objects.filter(receiver=user).count()
        notification_count2 = Notification.objects.filter(receiver=user).filter(notification_type=4).count()
        total = notification_count - notification_count2
        all_notf = Notification.objects.filter(receiver=user).values()
        for notf in all_notf:
            notf['sender_name'] = User.objects.get(pk=notf['sender_id']).username
        return JsonResponse({'notification_count': total, 'all_notfs':list(all_notf)})