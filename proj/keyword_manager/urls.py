# keyword_manager/urls.py
from django.urls import path
from .views import (FilteredAllScrappingListView,
                    FilteredAScrappingListView, 
                    KeywordCreateView, 
                    KeywordListView,
                    KeywordDeleteView,
                    DiscordMessageActiveUpdateView)

app_name = "keyword_manager"

urlpatterns = [
    path('filtered/', FilteredAllScrappingListView.as_view(), name='filtered_scrapping_list'),
    path('filtered/<str:keyword>/', FilteredAScrappingListView.as_view(), name='filtered_scrapping_list'),
    path('add/', KeywordCreateView.as_view(), name='add_keyword'),
    path('list/', KeywordListView.as_view(), name='keyword_list'),
    path('delete/<int:pk>/', KeywordDeleteView.as_view(), name='keyword_delete'),
    path('active/<int:pk>/', DiscordMessageActiveUpdateView.as_view(), name='active_update'),
    
]
