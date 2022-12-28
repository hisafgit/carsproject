from .models import Car
from rest_framework import serializers


class CarListSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()
    trans = serializers.StringRelatedField()
    extcolor = serializers.StringRelatedField()


    class Meta:      
        model= Car
        fields = ['title', 'price', 'img_url', 'brand', 'year', 'extcolor', 'trans']
