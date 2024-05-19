from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView
from .models import Keyword
from hotdeal.models import ScrappingModel  # Assuming 'hotdeal' is the app name for ScrappingModel
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import KeywordForm


class FilteredScrappingListView(LoginRequiredMixin, ListView):
    model = ScrappingModel
    template_name = 'keyword_manager/filtered_scrapping_list.html'
    context_object_name = 'scrapping_data'

    def get_queryset(self):
        user = self.request.user
        keywords = Keyword.objects.filter(user=user)
        keyword_texts = [keyword.text for keyword in keywords]

        if not keyword_texts:
            return ScrappingModel.objects.none()
        else:
            query = Q()
            for keyword in keyword_texts:
                query |= Q(title__icontains=keyword)
            return ScrappingModel.objects.filter(query, active=True)
        
class KeywordCreateView(LoginRequiredMixin, CreateView):
    model = Keyword
    template_name = 'keyword_manager/keyword_form.html'
    form_class = KeywordForm
    success_url = reverse_lazy('keyword_manager:keyword_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class KeywordDeleteView(LoginRequiredMixin, DeleteView):
    model = Keyword
    template_name = 'keyword_manager/keyword_delete.html'
    success_url = reverse_lazy('keyword_manager:keyword_list')


class KeywordListView(LoginRequiredMixin, ListView):
    model = Keyword
    template_name = 'keyword_manager/keyword_list.html'
    context_object_name = 'keywords'

    def get_queryset(self):
        user = self.request.user
        return Keyword.objects.filter(user=user)
    
# 내가 등록한키워드들 / 키워드 등록 / 키워드 검색 결과창 - O
# 키워드 결과창에 내 키워드 리스트 쭈루룩 뜨게 + 등록 url과 삭제 기능 만들기 O
# 등록창에 제약 걸수 있는지 + 중복된 키워드 안되게 + 특수문자 안되게 이런거