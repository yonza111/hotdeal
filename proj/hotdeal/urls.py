from django.urls import include, path
from .views import ScrappingModelViewSet


app_name = "hotdeal"


urlpatterns = [
     path('scrapping-list/', ScrappingModelViewSet.as_view({'get': 'list'}), name='scrapping_list'),
    ]