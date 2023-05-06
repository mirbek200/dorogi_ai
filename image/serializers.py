from rest_framework import serializers
from .models import RoadImage


class RoadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadImage
        fields = ['id', 'image']
