from django.urls import path
from post.views import CustomListView
from .views import CustomLoginView, CustomRegisterView, activate
from django.contrib.auth.views import LogoutView
from iface import settings
from notifications.models import Notification

app_name = 'authenticate'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='main_page'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    
    
    
    
    
    
]
