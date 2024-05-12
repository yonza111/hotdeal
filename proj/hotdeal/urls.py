from django.urls import include, path
from rest_framework import routers
from .views import ScrappingModelViewSet

app_name = "hotdeal"

router = routers.DefaultRouter()
router.register(r"list", ScrappingModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]