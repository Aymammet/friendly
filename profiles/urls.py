from django.urls import path
from .views import ProfileView, AcceptFriendRequest, ProfileEditView, SendFriendRequest, RemoveFriendView, UserSearchView ,AllFriendsView, RejectFriendRequest
app_name = 'profiles'

urlpatterns = [
    path('<int:pk>', ProfileView.as_view(), name='profile'),
    path('friends/add', AcceptFriendRequest.as_view(), name='add_friend'),
    path('edit/<int:pk>', ProfileEditView.as_view(), name='edit_profile'),
    path('send/<int:pk>', SendFriendRequest.as_view(), name='send_request' ),
    path('remove/<int:pk>', RemoveFriendView.as_view(), name='remove_friend' ),
    path('search', UserSearchView.as_view(), name='user_search' ),
    path('all_friends/', AllFriendsView.as_view(), name='all_friends'),
    path('reject/', RejectFriendRequest.as_view(), name='reject_friend_request' ),
]


