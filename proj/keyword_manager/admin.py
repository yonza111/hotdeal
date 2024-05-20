from django.contrib import admin
from .models import Keyword, DiscordMessage

class KeywordAdmin(admin.ModelAdmin):
    list_display = ['user', 'text']
    list_display_links = ['user']
admin.site.register(Keyword, KeywordAdmin)


class DiscordMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'discord_uid', 'active', 'keyword']
    list_display_links = ['user']
admin.site.register(DiscordMessage, DiscordMessageAdmin)