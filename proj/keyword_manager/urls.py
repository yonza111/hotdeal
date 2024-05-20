# keyword_manager/urls.py
from django.urls import path
from .views import (FilteredAllScrappingListView,
                    FilteredAScrappingListView, 
                    KeywordCreateView, 
                    KeywordListView,
                    KeywordDeleteView)

app_name = "keyword_manager"

urlpatterns = [
    path('filtered/', FilteredAllScrappingListView.as_view(), name='filtered_scrapping_list'),
    path('filtered/<str:keyword>/', FilteredAScrappingListView.as_view(), name='filtered_scrapping_list'),
    path('add/', KeywordCreateView.as_view(), name='add_keyword'),
    path('list/', KeywordListView.as_view(), name='keyword_list'),
    path('<int:pk>/delete/', KeywordDeleteView.as_view(), name='keyword_delete'),
]
