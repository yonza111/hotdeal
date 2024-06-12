# keyword_manager/urls.py
from django.urls import path
from .views import (FilteredAllScrappingListView,
                    FilteredAScrappingListView, 
                    KeywordCreateView, 
                    KeywordListView,
                    KeywordDeleteView,
                    DiscordMessageActiveUpdateView,)
                    # user_status)

app_name = "keyword_manager"

urlpatterns = [
    path('api/filtered/', FilteredAllScrappingListView.as_view(), name='filtered_scrapping_list'),
    path('api/filtered/<str:keyword>/', FilteredAScrappingListView.as_view(), name='filtered_scrapping_list'),
    path('api/add/', KeywordCreateView.as_view(), name='add_keyword'),
    path('api/list/', KeywordListView.as_view(), name='keyword_list'),
    path('api/delete/<int:pk>/', KeywordDeleteView.as_view(), name='keyword_delete'),
    path('api/active/<int:pk>/', DiscordMessageActiveUpdateView.as_view(), name='active_update'),
    # path('api/user_status/', user_status, name='user_status'),
]
