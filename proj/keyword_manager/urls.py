# keyword_manager/urls.py
from django.urls import path
from .views import (FilteredScrappingListView, 
                    KeywordCreateView, 
                    KeywordListView,
                    KeywordDeleteView)

app_name = "keyword_manager"

urlpatterns = [
    path('filtered/', FilteredScrappingListView.as_view(), name='filtered_scrapping_list'),
    path('add/', KeywordCreateView.as_view(), name='add_keyword'),
    path('list/', KeywordListView.as_view(), name='keyword_list'),
    path('<int:pk>/delete/', KeywordDeleteView.as_view(), name='keyword_delete'),
]
