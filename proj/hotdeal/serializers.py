# hotdeal/serializers.py

from rest_framework import serializers
from .models import ScrappingModel


class HotdealScrappingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrappingModel
        fields = '__all__'