from django.urls import path
from .views import PostNotification, RemoveNotification, RemoveNotification2,  RemoveNotification3


app_name = 'notifications'

urlpatterns = [

    path('notification/<int:notification_pk>/post/<int:post_pk>', PostNotification.as_view(), name='post_notification'),
    path('notificaion/delete/', RemoveNotification.as_view(), name='remove_notification'),
    path('notificaion/delete2/', RemoveNotification2.as_view(), name='remove_notification2'),
    path('notificaion/delete3/', RemoveNotification3.as_view(), name='remove_notification3'),
]

