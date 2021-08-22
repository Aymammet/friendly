from django.urls import path
from .views import ProfileView, JSONAddFriendView, RemoveFriendsView, ProfileEditView, Inbox, JsonMessages, JsonMessages_get

app_name = 'profiles'

urlpatterns = [
    path('<int:pk>', ProfileView.as_view(), name='profile'),
    path('friends/add', JSONAddFriendView.as_view(), name='add_friend'),
    path('<int:pk>/friends/remove', RemoveFriendsView.as_view(), name='remove_friend'),
    path('edit/<int:pk>', ProfileEditView.as_view(), name='edit_profile'),
    path('inbox/', Inbox.as_view(), name='inbox'),
    path('inbox/messages', JsonMessages.as_view(), name='messages'),
    path('inbox/messages/get', JsonMessages_get.as_view(), name='get_messages'),
    
    # path('inbox/create_thread/', CreateThread.as_view(), name='create_thread'),
    # path('inbox/<int:pk>/', ThreadView.as_view() , name='thread'),
    # path('inbox/create-message', CreateMessage.as_view() , name='create-message'),
    # path('inbox/create-message-js', CreateMessageJs.as_view() , name='create-message-js'),
    # path('inbox/delete_thread', DeleteThread.as_view() , name='delete_thread'),

]


