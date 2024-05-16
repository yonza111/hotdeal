from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from .models import ScrappingModel
from .serializers import ScrappingModelSerializer
from django.shortcuts import render, get_object_or_404


def main(request):
    return render(request, 'main_view.html')


class ScrappingListView(ListView):
    model = ScrappingModel
    template_name = 'scrapping_list.html'
    context_object_name = 'page_obj'
    paginate_by = 20
    ordering = '-register_time'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = context['paginator'].get_page(self.request.GET.get('page'))
        return context
'''템플릿에서 page_obj 변수를 사용하여 페이지네이션을 출력하고 있음에도 불구하고 
페이지네이션 정보가 출력되지 않는다면, 
추가적으로 get_context_data() 메서드를 사용하여 
컨텍스트에 페이지네이션 정보를 전달해야 할 수도 있습니다'''

class CategoryListView(ListView):
    model = ScrappingModel
    template_name = 'category_list.html'
    context_object_name = 'page_obj'
    ordering = '-register_time'

    def get_queryset(self):
        category = self.kwargs.get('category')
        querySet = ScrappingModel.objects.filter(category=category)
        return querySet
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs['category']
        context['category'] = category
        return context
    
    #  어떻게 한건지모르겠음;ㅋ


class ScrappingSearchListView(ListView):
    model = ScrappingModel
    template_name = 'scrapping_search_list.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ScrappingDetailView(DetailView):
    model = ScrappingModel
    template_name = 'scrapping_detail.html'
    context_object_name = 'post'

