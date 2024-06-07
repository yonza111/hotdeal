from django.urls import include, path
from .views import (ScrappingListView, 
                    main, 
                    ScrappingDetailView, 
                    CategoryListView, 
                    ScrappingSearchListView,) 

app_name = "hotdeal"


urlpatterns = [
    path('', main, name='main'),
    path('list/', ScrappingListView.as_view(), name='list'),
    path('list/<int:pk>/', ScrappingDetailView.as_view(), name='detail'),
    path('category/<path:category>/', CategoryListView.as_view(), name='category_list'),
    path('search/', ScrappingSearchListView.as_view(), name='search'),
]


# urlpatterns = [
#     path('', main, name='main'),
#     path('list/', ScrappingListView.as_view(), name='list'),
#     path('list/<int:pk>/', ScrappingDetailView.as_view(), name='detail'),
#     path('category/<path:category>/', CategoryListView.as_view(), name='category_list'),
#     path('search/', ScrappingSearchListView.as_view(), name='search'),
#     ]