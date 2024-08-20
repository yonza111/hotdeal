# accounts/urls.py



from django.urls import path
from .views import DiscordCallbackView

urlpatterns = [
    path('callback/', DiscordCallbackView.as_view(), name='discord_login_callback'),
]
