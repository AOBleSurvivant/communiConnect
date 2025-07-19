from rest_framework import serializers
from .models import Region, Prefecture, Commune, Quartier

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'nom', 'code']

class PrefectureSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    class Meta:
        model = Prefecture
        fields = ['id', 'nom', 'code', 'region']

class CommuneSerializer(serializers.ModelSerializer):
    prefecture = PrefectureSerializer(read_only=True)
    class Meta:
        model = Commune
        fields = ['id', 'nom', 'code', 'type', 'prefecture']

class QuartierSerializer(serializers.ModelSerializer):
    commune = CommuneSerializer(read_only=True)
    class Meta:
        model = Quartier
        fields = ['id', 'nom', 'code', 'commune', 'population_estimee', 'superficie_km2'] 