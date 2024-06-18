# keyword_manager/serializers.py
from rest_framework import serializers
from .models import Keyword, DiscordMessage
from hotdeal.models import ScrappingModel


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id','text']

class ScrappingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrappingModel
        fields = '__all__'

class DiscordMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscordMessage
        fields = ['active']
