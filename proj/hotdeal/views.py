from rest_framework import viewsets
from django.shortcuts import render
from .models import ScrappingModel
from .serializers import ScrappingModelSerializer

class ScrappingModelViewSet(viewsets.ModelViewSet):
    queryset = ScrappingModel.objects.all()
    serializer_class = ScrappingModelSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        context = {
            'scrappings': serializer.data
        }
        return render(request, 'scrapping_list.html', context)

from django.shortcuts import render, get_object_or_404

def scrapping_detail_view(request, scrapping_id):
    scrapping = get_object_or_404(ScrappingModel, pk=scrapping_id)
    return render(request, 'scrapping_detail.html', {'scrapping':scrapping})