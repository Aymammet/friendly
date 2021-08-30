from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from post.models import Post
from notifications.models import Notification 
from django.views.generic import View, UpdateView
from django.urls import reverse_lazy
import json
from django.http import JsonResponse
from django.db.models import Q
from dm.models import Room
from .form import UpdateProfileForm 


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = User.objects.get(pk=pk)
        username = profile.username
        posts = Post.objects.filter(owner_of_post=profile.id).order_by('-created_date')
        posts_all =  Post.objects.all()
        is_friend = False        
        if self.request.user in profile.friends.all():
            is_friend = True
        context = {
            'user2' : username,
            'profile' : profile,
            'posts' : posts,
            'number_of_friends' : profile.friends.count(),
            'is_friend' : is_friend,
        }
        return render(request, 'profile.html', context)

class ProfileEditView(UpdateView):
    model = User
    fields = ['name', 'surname', 'birth_date', 'image', 'bio', 'username' ]
    template_name = 'profile_edit.html'
    form = UpdateProfileForm
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profiles:profile', kwargs={'pk':pk})        

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


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


class AllFriendsView(View):
    template_name = 'all_friends.html'
    def get(self, request):
        return render(request, self.template_name)


class SendFriendRequest(View):
    def post(self, request, pk,  *args, **kwargs):
        add_friend = get_object_or_404(User, pk=pk)
        Notification.objects.create(notification_type=3, sender=request.user, receiver=add_friend)
        return redirect('profiles:profile', pk=pk)

def create_room(user1_id, user2_id):
    users = sorted([user1_id, user2_id])
    return int('0'.join([str(users[0]), str(users[1])]))


class AcceptFriendRequest(View):
    def post(self, request):
        body = json.loads(request.body)
        user = request.user
        friend = get_object_or_404(User, id = body['sender'])
        notification = Notification.objects.get(pk=body['p_not']) 
        notification.remove_notification()
        user.friends.add(friend)
        friend.friends.add(user)
        Room.objects.create(room_id = create_room(user.pk, friend.pk))
        return JsonResponse({})


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
        return redirect('profiles:all_friends')


class RejectFriendRequest(View):
    def post(self, request):
        body = json.loads(request.body)
        p_not = body['p_not']
        notification = Notification.objects.get(pk=p_not)
        notification.remove_notification()
        return JsonResponse({})




















# class ListThreads(View):
#     def get(self, request, *args, **kwargs):
#         threads = Thread.objects.filter(Q(user=request.user) | Q(receiver=request.user))
#         form = ThreadForm()
#         context = {
#             'threads' : threads,
#             'form' : form
#         }
#         return render(request, 'inbox.html', context)

#     def post(self, request, *args, **kwargs):
#         form = ThreadForm(request.POST)
#         username = request.POST.get('username')
#         user = User.objects.get(username=request.user.username)
#         try:
#             user2 = User.objects.get(username=username)
#         except:
#             messages.error(request, 'Invalid username')
#             return redirect('profiles:inbox')
#         if user in user2.friends.all():
#             pass
#         else:
#             messages.error(request, 'This user is not your friend yet')
#             return redirect('profiles:inbox')
            
#         # if User.objects.filter(username=request.user, friends=username).exists():
#         #     print(3)
#         # else:
#         #     print(4)
#         try:
#             receiver = User.objects.get(username=username)
#             if Thread.objects.filter(user=request.user, receiver=receiver).exists():
#                 thread = Thread.objects.filter(user=request.user, receiver=receiver)[0]
#                 return redirect('profiles:thread', pk=thread.pk)
#             elif Thread.objects.filter(user=receiver, receiver=request.user).exists():
#                 thread = Thread.objects.filter(user=receiver, receiver=request.user)[0]
#                 return redirect('profiles:thread', pk=thread.pk)
#             if form.is_valid():
#                 thread = Thread(
#                     user = request.user,
#                     receiver = receiver
#                 )
#                 thread.save()
#                 return redirect('profiles:thread', pk=thread.pk)
#         except:
#             messages.error(request, 'Invalid username')
#             return redirect('profiles:create_thread')


# class CreateThread(View):
#     def get(self, request, *args, **kwargs):
#         form = ThreadForm()
#         context = {
#             'form' : form
#         }
#         return render(request, 'create_thread.html', context)
    
#     def post(self, request, *args, **kwargs):
#         form = ThreadForm(request.POST)
#         username = request.POST.get('username')
#         user = User.objects.get(username=request.user.username)
#         try:
#             user2 = User.objects.get(username=username)
#         except:
#             messages.error(request, 'Invalid username')
#             return redirect('profiles:create_thread')
#         if user in user2.friends.all():
#             pass
#         else:
#             messages.error(request, 'This user is not your friend yet')
#             return redirect('profiles:create_thread')
            
#         # if User.objects.filter(username=request.user, friends=username).exists():
#         #     print(3)
#         # else:
#         #     print(4)
#         try:
#             receiver = User.objects.get(username=username)
#             if Thread.objects.filter(user=request.user, receiver=receiver).exists():
#                 thread = Thread.objects.filter(user=request.user, receiver=receiver)[0]
#                 return redirect('profiles:thread', pk=thread.pk)
#             elif Thread.objects.filter(user=receiver, receiver=request.user).exists():
#                 thread = Thread.objects.filter(user=receiver, receiver=request.user)[0]
#                 return redirect('profiles:thread', pk=thread.pk)
#             if form.is_valid():
#                 thread = Thread(
#                     user = request.user,
#                     receiver = receiver
#                 )
#                 thread.save()
#                 return redirect('profiles:thread', pk=thread.pk)
#         except:
#             messages.error(request, 'Invalid username')
#             return redirect('profiles:create_thread')


# class ThreadView(View):
#     def get(self, request, pk,  *args, **kwargs):
#         form_message = MessageForm()
#         thread = Thread.objects.get(pk=pk)
#         message_list = MessageModel.objects.filter(thread__pk__contains=pk)
#         threads = Thread.objects.filter(Q(user=request.user) | Q(receiver=request.user))
#         form = ThreadForm()
#         context = {
#             'thread': thread,
#             'form_message' : form_message,
#             'message_list' : message_list,
#             'threads' : threads,
#             'form' : form
#         }
#         return render(request, 'inbox.html', context)

#         form = ThreadForm(request.POST)
#         username = request.POST.get('username')
#         user = User.objects.get(username=request.user.username)
#         try:
#             user2 = User.objects.get(username=username)
#         except:
#             messages.error(request, 'Invalid username')
#             return redirect('profiles:inbox')
#         if user in user2.friends.all():
#             pass
#         else:
#             messages.error(request, 'This user is not your friend yet')
#             return redirect('profiles:inbox')
            
#         # if User.objects.filter(username=request.user, friends=username).exists():
#         #     print(3)
#         # else:
#         #     print(4)
#         try:
#             receiver = User.objects.get(username=username)
#             if Thread.objects.filter(user=request.user, receiver=receiver).exists():
#                 thread = Thread.objects.filter(user=request.user, receiver=receiver)[0]
#                 return redirect('profiles:thread', pk=thread.pk)
#             elif Thread.objects.filter(user=receiver, receiver=request.user).exists():
#                 thread = Thread.objects.filter(user=receiver, receiver=request.user)[0]
#                 return redirect('profiles:thread', pk=thread.pk)
#             if form.is_valid():
#                 thread = Thread(
#                     user = request.user,
#                     receiver = receiver
#                 )
#                 thread.save()
#                 return redirect('profiles:inbox', pk=thread.pk)
#         except:
#             messages.error(request, 'Invalid username')
#             return redirect('profiles:inbox')


# class CreateMessage(View):
#     def post(self, request):
#         body = json.loads(request.body)
#         thread = Thread.objects.get(pk=body['thread_pk'])
#         message = body['message']
#         if thread.receiver == request.user:
#             receiver = thread.user
#         else:
#             receiver = thread.receiver
#         message = MessageModel(
#             thread=thread,
#             sender_user = request.user,
#             receiver_user = receiver,
#             body = message
#         )
#         message.save()

#         all_messages = MessageModel.objects.filter(thread=thread).values()
#         for message in all_messages:
#             message['sender_name'] = User.objects.get(pk=message['sender_user_id']).username
#             message['receiver_name'] = User.objects.get(pk=message['receiver_user_id']).username

#         notification = Notification.objects.create(
#             notification_type=4,
#             sender = request.user,
#             receiver = receiver,
#             thread = thread
#             )
#         return JsonResponse({'messages': list(all_messages)})
      

# class CreateMessageJs(View):
#     def post(self, request):
#         body = json.loads(request.body)
#         thread = Thread.objects.get(pk=body['thread_pk'])
#         if thread.receiver == request.user:
#             receiver = thread.user
#         else:
#             receiver = thread.receiver
#         all_messages = MessageModel.objects.filter(thread=thread).values()
#         for message in all_messages:
#             message['sender_name'] = User.objects.get(pk=message['sender_user_id']).username
#             message['receiver_name'] = User.objects.get(pk=message['receiver_user_id']).username
#         return JsonResponse({'messages': list(all_messages)})


# class DeleteThread(View):
#     def post(self, request, *args, **kwargs):
#         pk = request.GET.get('delete')
#         thread = Thread.objects.get(pk=pk)
#         thread.remove()
#         return redirect('profiles:inbox')
        