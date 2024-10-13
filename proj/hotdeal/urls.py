# hotdeal/urls.py
from django.urls import path
from .views import (ScrappingListView,
                    ScrappingDetailView, 
                    CategoryListView, 
                    ScrappingSearchListView,) 

app_name = "hotdeal"


urlpatterns = [
    path('api/scrappinglist/', ScrappingListView.as_view(), name='list'),
    path('api/scrappinglist/<int:pk>/', ScrappingDetailView.as_view(), name='detail'),
    path('api/category/<path:category>/', CategoryListView.as_view(), name='category_list'),
    path('api/search/', ScrappingSearchListView.as_view(), name='search'),
]
