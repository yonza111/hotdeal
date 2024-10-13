# keyword_manager/views.py
from rest_framework import generics, permissions
from .models import Keyword, DiscordMessage
from hotdeal.models import ScrappingModel
from .serializers import KeywordSerializer, ScrappingModelSerializer, DiscordMessageSerializer
from rest_framework.response import Response


class KeywordListView(generics.ListAPIView):
    serializer_class = KeywordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Keyword.objects.filter(user=user)


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


class DiscordMessageActiveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = DiscordMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = DiscordMessage.objects.all()
    lookup_field = 'pk'

    def get_object(self):
        # user의 Discord 메시지 객체를 가져옴
        user = self.request.user
        queryset = self.get_queryset()
        obj = queryset.filter(user=user).first()

        if not obj:
            # Discord 메시지가 없는 경우 404 응답을 반환
            return Response({"Discord message does not exist"}, status=404)

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
