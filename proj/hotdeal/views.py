# hotdeal/views.py
from rest_framework import generics
from django.shortcuts import render
from .models import ScrappingModel
from .serializers import HotdealScrappingModelSerializer


class ScrappingListView(generics.ListAPIView):
    queryset = ScrappingModel.objects.filter(active=True).order_by('-register_time')
    serializer_class = HotdealScrappingModelSerializer


class CategoryListView(generics.ListAPIView):
    serializer_class = HotdealScrappingModelSerializer

    def get_queryset(self):
        category = self.kwargs.get('category')
        return ScrappingModel.objects.filter(category=category, active=True).order_by('-register_time')


class ScrappingSearchListView(generics.ListAPIView):
    serializer_class = HotdealScrappingModelSerializer

    def get_queryset(self):
        search_query = self.request.GET.get('q', '') # '' <- default 값.
        queryset = ScrappingModel.objects.all()
        if search_query:
            queryset = queryset.filter(title__icontains=search_query, active=True)
        return queryset.order_by('-register_time')


class ScrappingDetailView(generics.RetrieveAPIView):
    queryset = ScrappingModel.objects.all()
    serializer_class = HotdealScrappingModelSerializer
    lookup_field = 'pk'