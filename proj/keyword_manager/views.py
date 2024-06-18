# keyword_manager/views.py

from rest_framework import generics, permissions
from django.urls import reverse_lazy
from .models import Keyword, DiscordMessage
from hotdeal.models import ScrappingModel
from django.db.models import Q
from .serializers import KeywordSerializer, ScrappingModelSerializer, DiscordMessageSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response


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

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     user = self.request.user
    #     discord_message = DiscordMessage.objects.filter(user=user).first()
    #     response.data.append({
    #         'discord_message_active': discord_message.active if discord_message else False,
    #         'discord_message_pk': discord_message.pk if discord_message else None
    #     })
    #     return response   # 왜 있었지?;


class DiscordMessageActiveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = DiscordMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = DiscordMessage.objects.all()
    lookup_field = 'pk'

    def get_object(self):
        # 사용자와 관련된 Discord 메시지 객체를 가져옵니다.
        user = self.request.user
        queryset = self.get_queryset()
        obj = queryset.filter(user=user).first()

        if not obj:
            # Discord 메시지가 없는 경우 404 응답을 반환합니다.
            return Response({"detail": "Discord message does not exist for this user."}, status=404)

        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_queryset(self):
        user = self.request.user
        return DiscordMessage.objects.filter(user=user) # 내 것만

    def put(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # 현재 active 상태의 반대로 변경
        for discord_message in queryset:
            discord_message.active = not discord_message.active
            discord_message.save()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
