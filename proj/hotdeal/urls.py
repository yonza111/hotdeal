from django.urls import include, path
from .views import ScrappingModelListView, board, detail

app_name = "hotdeal"


urlpatterns = [
    path('api/scrapping-list/', ScrappingModelListView.as_view(), name='scrapping-list'),
    path('board/', board, name='board'),
    path('board/<int:pk>/', detail, name='detail'),
     ]