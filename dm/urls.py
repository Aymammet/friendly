from django.urls import path
from .views import Inbox, JsonMessages, JsonMessages_get

app_name = 'dm'

urlpatterns = [
    path('inbox/', Inbox.as_view(), name='inbox'),
    path('inbox/messages', JsonMessages.as_view(), name='messages'),
    path('inbox/messages/get', JsonMessages_get.as_view(), name='get_messages'),
]


