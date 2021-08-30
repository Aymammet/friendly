from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, View
from .models import Post, Comments
from profiles.models import User
from notifications.models import Notification
from .forms import CreatePostForm, CommentForm
from django.utils import timezone
from django.http import JsonResponse
import json
from django.contrib import messages
from operator import attrgetter
from itertools import chain


class CustomListView(ListView):
    template_name = 'home.html'
    model = Post
    context_object_name = 'posts'
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            self.template_name = 'main_page'
        else:
            if self.request.user.username == 'admin':
                return Post.objects.all().order_by('-created_date')
            else:
                merged_list = sorted(
                        chain(Post.objects.filter(owner_of_post__in= self.request.user.friends.all()), Post.objects.filter(owner_of_post = self.request.user)),
                        key=attrgetter('created_date'), reverse=True)
                return merged_list
               
               
    def get_context_data(self, **kwargs):
       context = super(CustomListView, self).get_context_data(**kwargs)
       context['commentform'] = CommentForm()
       return context

    
class CustomCreateView(CreateView):
    form_class = CreatePostForm
    template_name = 'new_post.html'
    model =  Post
    success_url = reverse_lazy('post:home')
    error_message = 'Please post something or add image'
    
    def form_valid(self, form):
        myobj = form.save(commit=False)
        myobj.owner_of_post = self.request.user
        myobj.created_date = timezone.now()
        if not myobj.description and not myobj.image:
            messages.error(self.request, self.error_message)
            return redirect('post:new_post')
        return super().form_valid(form)


class CustomUpdateView(UpdateView):
    form_class = CreatePostForm
    model = Post
    template_name = 'edit_post.html'
    context_object_name = 'current'
    success_url = reverse_lazy('post:home')
    

class CustomDeleteView(DeleteView):
    template_name = 'delete_post.html'
    model = Post
    success_url = reverse_lazy('post:home')


class CustomDetailView(DetailView):
    template_name = 'post_detail.html'
    model = Post

    def get_context_data(self, **kwargs):
       context = super(CustomDetailView, self).get_context_data(**kwargs)
       context['commentform'] = CommentForm()
       return context

    def post(self, request, pk):
       post = get_object_or_404(Post, pk=pk)
       form = CommentForm(request.POST)

       if form.is_valid():
           obj  = form.save(commit=False)
           obj.post = post
           obj.owner_of_comments = self.request.user
           obj.created_date = timezone.now()
           obj.save()
           return redirect('post:post_detail', post.pk)

    
class CustomCommentView(View):
    http_method_names = ['post']
    def post(self, request):
        body = json.loads(request.body)
        post = get_object_or_404(Post, pk=body['post_pk'])
        new_comment = body['comment']
        Comments.objects.create(owner_of_comments=request.user, post=post, created_date=timezone.now(), comment=new_comment)
        Notification.objects.create(notification_type=2, sender=request.user, receiver=post.owner_of_post, post=post)
        all_comments = Comments.objects.filter(post=post).values()
        
        for comment in all_comments:
            comment['owner_of_comment'] = User.objects.get(pk=comment['owner_of_comments_id']).username
            comment['owner_of_comment_image'] = User.objects.get(pk=comment['owner_of_comments_id']).get_profile_image()
        return JsonResponse({'all_comments':list(all_comments) , 'number_of_comments': Comments.objects.filter(post=post).count(), 'new_comment': new_comment, 'comm_date': timezone.now() })
        

class CustomLikeView(View):
    http_method_names = ['post']
    def post(self, request):
        body = json.loads(request.body)
        post = get_object_or_404(Post, pk=body['post_pk'])
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            state = 'no-like'
        else:
            post.dislikes.remove(request.user)
            post.likes.add(request.user)
            state = 'yes-like'
            Notification.objects.create(notification_type=1, sender=request.user, receiver=post.owner_of_post, post=post)
        return JsonResponse({'likes': post.likes.count(), 'post_id':post.id, 'dislikes':post.dislikes.count(), 'state':state})


class CustomDislikeView(View):
    http_method_names = ['post']
    def post(self, request):
        body = json.loads(request.body)
        post = get_object_or_404(Post, pk=body['disliked_post_pk'])
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
            state = 'no-dislike'
        else:
            post.likes.remove(request.user)
            post.dislikes.add(request.user)
            state = 'yes-dislike'
        return JsonResponse({'dislikes': post.dislikes.count(), 'dislike_post_id':post.pk, 'likes':post.likes.count(), 'state':state})




