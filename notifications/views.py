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


class AddFriend(View):
    def post(self, request):
        body = json.loads(request.body)
        
        p_sen = body['p_sen']
        p_rec = body['p_rec']
        p_not = body['p_not']
        
        add_friend = get_object_or_404(User, pk=p_sen)
        user = User.objects.get(pk=p_rec)
        user.friends.add(add_friend)
        add_friend.friends.add(user)
        notification = Notification.objects.get(pk=p_not)
        
        # notification.user_has_seen = True
        # notification.save()
        notification.remove_notification()
        
        return render(request, 'home.html')


class ThreadNotification(View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = Thread.objects.get(pk=object_pk)
        notification.user_has_seen = True
        notification.save()
        notification.remove_notification()
        return redirect('profiles:thread', pk=thread.pk)


class RemoveNotification(View):
    def post(self, request):
        body = json.loads(request.body)
        notification = Notification.objects.get(pk=body['notf_pk'])
        notification.user_has_seen = True
        notification.save()
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

class SendRequestAddFriendView(View):

    def post(self, request, pk,  *args, **kwargs):
        add_friend = get_object_or_404(User, pk=pk)
        Notification.objects.create(notification_type=3, sender=request.user, receiver=add_friend)
        return redirect('profiles:profile', pk=pk)

class CancelRequestAddFriendView(View):

    def post(self, request, pk,  *args, **kwargs):
        friend = get_object_or_404(User, pk=pk)
        # user = User.objects.get(pk=self.request.user.pk)
        Notification.objects.filter(notification_type=3, sender=request.user, receiver=friend)
        return redirect('profiles:profile', pk=pk)


class RemoveFriendView(View):

    def post(self, request, pk,  *args, **kwargs):
        removed_friend = get_object_or_404(User, pk=pk)
        user = User.objects.get(pk=self.request.user.pk)
        user.friends.remove(removed_friend)
        removed_friend.friends.remove(user)
        return redirect('notifications:all_friends')


class UserSearchView(View):

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        if query == '':
             return render(request, 'friends.html')
        else:
            profile_list = User.objects.filter(
                Q(username__startswith=query)
            )
            context = {
                'profile_list' : profile_list
             }
        return render(request, 'friends.html', context)


class UserSearchViewMain(View):

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        if query == '':
             return render(request, 'home.html')
        else:
            profile_list = User.objects.filter(
                Q(username__startswith=query)
            )
            context = {
                'profile_list' : profile_list
             }
        return render(request, 'home.html', context)


# class FriendsView(View):
#     template_name = 'friends.html'

#     def get(self, request):
#         return render(request, self.template_name)

class AllFriendsView(View):
    template_name = 'all_friends.html'

    def get(self, request):
        return render(request, self.template_name)





class RejectFriendRequest(View):

    def post(self, request):
        body = json.loads(request.body)
        p_not = body['p_not']
        notification = Notification.objects.get(pk=p_not)
        notification.user_has_seen = True
        notification.remove_notification()
        return redirect('post:home')
    