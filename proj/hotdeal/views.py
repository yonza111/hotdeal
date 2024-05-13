from rest_framework import generics
from .models import ScrappingModel
from .serializers import ScrappingModelSerializer
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator


class ScrappingModelListView(generics.ListAPIView):
    queryset = ScrappingModel.objects.all()
    serializer_class = ScrappingModelSerializer

def board(request):
    all_hotdeals = ScrappingModel.objects.all()
    posts_per_page = 20
    paginator = Paginator(all_hotdeals, posts_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'scrapping_list.html', {'page_obj': page_obj})

def detail(request, pk):
    post = get_object_or_404(ScrappingModel, pk=pk)
    return render(request, 'scrapping_detail.html', {'post': post})