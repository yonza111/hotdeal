from django.urls import include, path
from .views import (ScrappingListView, 
                    index, 
                    ScrappingDetailView, 
                    CategoryListView, 
                    ScrappingSearchListView,) 

app_name = "hotdeal"


urlpatterns = [
    path('', index, name='index'),
    path('api/scrappinglist/', ScrappingListView.as_view(), name='list'),
    path('api/scrappinglist/<int:pk>/', ScrappingDetailView.as_view(), name='detail'),
    path('api/category/<path:category>/', CategoryListView.as_view(), name='category_list'),
    path('api/search/', ScrappingSearchListView.as_view(), name='search'),
]


# urlpatterns = [
#     path('', main, name='main'),
#     path('list/', ScrappingListView.as_view(), name='list'),
#     path('list/<int:pk>/', ScrappingDetailView.as_view(), name='detail'),
#     path('category/<path:category>/', CategoryListView.as_view(), name='category_list'),
#     path('search/', ScrappingSearchListView.as_view(), name='search'),
#     ]