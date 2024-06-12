# keyword_manager/views.py

from rest_framework import generics, permissions
from django.urls import reverse_lazy
from .models import Keyword, DiscordMessage
from hotdeal.models import ScrappingModel
from django.db.models import Q
from .serializers import KeywordSerializer, ScrappingModelSerializer, DiscordMessageSerializer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


class FilteredAllScrappingListView(generics.ListAPIView):
    serializer_class = ScrappingModelSerializer
    permission_classes = [permissions.IsAuthenticated]

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


class FilteredAScrappingListView(generics.ListAPIView):
    serializer_class = ScrappingModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        keyword_text = self.kwargs.get('keyword')
        return ScrappingModel.objects.filter(title__icontains=keyword_text, active=True)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data.append({'keyword': self.kwargs.get('keyword')})
        return response


class KeywordCreateView(generics.CreateAPIView):
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class KeywordDeleteView(generics.DestroyAPIView):
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Keyword.objects.filter(user=user)


class KeywordListView(generics.ListAPIView):
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Keyword.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        user = self.request.user
        discord_message = DiscordMessage.objects.filter(user=user).first()
        response.data.append({
            'discord_message_active': discord_message.active if discord_message else False,
            'discord_message_pk': discord_message.pk if discord_message else None
        })
        return response


class DiscordMessageActiveUpdateView(generics.UpdateAPIView):
    serializer_class = DiscordMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = DiscordMessage.objects.all()
    lookup_field = 'pk'

    def get_success_url(self):
        return reverse_lazy('keyword_manager:keyword_list')
