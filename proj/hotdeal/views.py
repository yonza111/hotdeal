from rest_framework import viewsets
from .models import ScrappingModel
from .serializers import ScrappingModelSerializer

class ScrappingModelViewSet(viewsets.ModelViewSet):
    queryset = ScrappingModel.objects.all()
    serializer_class = ScrappingModelSerializer