from rest_framework import generics
from django.shortcuts import render
from .models import ScrappingModel
from .serializers import ScrappingModelSerializer
from rest_framework.pagination import PageNumberPagination


def index(request):
    return render(request, 'index.html')


class ScrappingListView(generics.ListAPIView):
    queryset = ScrappingModel.objects.all().order_by('-register_time')
    serializer_class = ScrappingModelSerializer
    # pagination_class = PageNumberPagination  # 페이지네이션 클래스 지정
    # page_size = 20  


class CategoryListView(generics.ListAPIView):
    serializer_class = ScrappingModelSerializer

    def get_queryset(self):
        category = self.kwargs.get('category')
        return ScrappingModel.objects.filter(category=category).order_by('-register_time')


class ScrappingSearchListView(generics.ListAPIView):
    serializer_class = ScrappingModelSerializer

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        queryset = ScrappingModel.objects.all()
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset.order_by('-register_time')


class ScrappingDetailView(generics.RetrieveAPIView):
    queryset = ScrappingModel.objects.all()
    serializer_class = ScrappingModelSerializer
    lookup_field = 'pk'