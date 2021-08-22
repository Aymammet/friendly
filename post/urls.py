from django.urls import path
from .views import CustomListView, CustomLikeView, CustomDislikeView, CustomCreateView, CustomLikeView, CustomUpdateView, CustomDeleteView, CustomUpdateView, CustomDetailView, CustomCommentView


app_name = 'post'

urlpatterns = [
    path('', CustomListView.as_view(), name='home'),
    path('new_post', CustomCreateView.as_view(), name='new_post'),
    path('<int:pk>/edit_post', CustomUpdateView.as_view(), name='edit_post'),
    path('<int:pk>/delete_post', CustomDeleteView.as_view(), name='delete_post'),
    path('<int:pk>/post_detail', CustomDetailView.as_view(), name='post_detail'),
    path('comment', CustomCommentView.as_view(), name='comment'),
    path('like', CustomLikeView.as_view(), name='post_like'),
    path('dislike', CustomDislikeView.as_view(), name='post_dislike'),
   
]
