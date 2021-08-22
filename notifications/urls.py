from django.urls import path
from .views import PostNotification, AddFriend, AllFriendsView, RemoveNotification, RemoveNotification2,  RemoveNotification3, SendRequestAddFriendView, RemoveFriendView, UserSearchView, UserSearchViewMain, RejectFriendRequest, ThreadNotification
from profiles.views import JSONAddFriendView

app_name = 'notifications'

urlpatterns = [

    path('notification/<int:notification_pk>/post/<int:post_pk>', PostNotification.as_view(), name='post_notification'),
    path('notificaion/delete/', RemoveNotification.as_view(), name='remove_notification'),
    path('notificaion/delete2/', RemoveNotification2.as_view(), name='remove_notification2'),
    path('notificaion/delete3/', RemoveNotification3.as_view(), name='remove_notification3'),
    path('notification/add/' ,  JSONAddFriendView.as_view(), name='add_friend' ),
    path('notification/send/<int:pk>', SendRequestAddFriendView.as_view(), name='send_request' ),
    path('notifications/remove/<int:pk>', RemoveFriendView.as_view(), name='remove_friend' ),
    path('notifications/search', UserSearchView.as_view(), name='user_search' ),
    path('notifications/find/', UserSearchViewMain.as_view(), name='user_search_main' ),
    path('notifications/all_friends/', AllFriendsView.as_view(), name='all_friends'),
    path('notifications/reject/', RejectFriendRequest.as_view(), name='reject_friend_request' ),
    path('notifications/<int:notification_pk>/thread/<int:object_pk>', ThreadNotification.as_view(), name='thread_notification' ),
]

