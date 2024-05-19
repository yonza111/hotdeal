# keyword_manager/urls.py
from django.urls import path
from .views import FilteredScrappingListView, KeywordCreateView

urlpatterns = [
    path('filtered/', FilteredScrappingListView.as_view(), name='filtered_scrapping_list'),
    path('add/', KeywordCreateView.as_view(), name='add_keyword'),
]
