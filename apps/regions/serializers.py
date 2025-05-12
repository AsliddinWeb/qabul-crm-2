from rest_framework import serializers
from .models import Country, Region, District


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'country']


class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = District
        fields = ['id', 'name', 'region']
