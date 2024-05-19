from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
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
    success_url = reverse_lazy('keyword_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)