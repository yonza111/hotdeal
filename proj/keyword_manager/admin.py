from django.contrib import admin
from .models import Keyword

class KeywordAdmin(admin.ModelAdmin):
    list_display = ['user', 'text']
    list_display_links = ['user']
admin.site.register(Keyword, KeywordAdmin)