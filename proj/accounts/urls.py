# accounts/urls.py

from django.urls import path
from .views import discord_callback

urlpatterns = [
    path('discord/callback/', discord_callback, name='discord_login_callback'),
]
