from rest_framework import serializers
from .models import ScrappingModel


class ScrappingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrappingModel
        fields = '__all__'