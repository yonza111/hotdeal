from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Keyword, DiscordMessage
from hotdeal.models import ScrappingModel  # Assuming 'hotdeal' is the app name for ScrappingModel
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import KeywordForm

class FilteredAllScrappingListView(LoginRequiredMixin, ListView):
    model = ScrappingModel
    template_name = 'keyword_manager/filtered_all_scrapping_list.html'
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
        

class FilteredAScrappingListView(LoginRequiredMixin, ListView):
    model = ScrappingModel
    template_name = 'keyword_manager/filtered_a_scrapping_list.html'
    context_object_name = 'scrapping_data'

    def get_queryset(self):
        keyword_text = self.kwargs.get('keyword')
        return ScrappingModel.objects.filter(title__icontains=keyword_text, active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword'] = self.kwargs.get('keyword') 
        return context
     # list template에서 keyword = data.text로 가져옴    
        
class KeywordCreateView(LoginRequiredMixin, CreateView):
    model = Keyword
    template_name = 'keyword_manager/keyword_form.html'
    form_class = KeywordForm
    success_url = reverse_lazy('keyword_manager:keyword_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        discord_message = DiscordMessage.objects.filter(user=user).first()
        context['discord_message_active'] = discord_message.active if discord_message else False
        context['discord_message_pk'] = discord_message.pk if discord_message else None
        return context


class DiscordMessageActiveUpdateView(LoginRequiredMixin, UpdateView):
    model = DiscordMessage
    context_object_name = 'object'
    fields = ['active']
    template_name='keyword_manager/discord_message_active.html'
    success_url = reverse_lazy('keyword_manager:keyword_list')