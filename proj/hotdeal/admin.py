from django.contrib import admin
from .models import ScrappingModel

# 이후 기능 확장을 위해 관리자가 직접 비활성화 할 수 있게 만듦.
def deactivate(modeladmin, request, queryset):
    queryset.update(active=False)
deactivate.short_description = "해당 데이터 비활성화"

class ScrappingModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'register_time', 'active']
    list_display_links = ['title']
    list_filter = ['category']
    search_fields = ['title']
    actions = [deactivate]
admin.site.register(ScrappingModel, ScrappingModelAdmin)