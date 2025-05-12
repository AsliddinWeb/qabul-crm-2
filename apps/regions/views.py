from rest_framework import generics, permissions
from .models import Country, Region, District
from .serializers import CountrySerializer, RegionSerializer, DistrictSerializer


# --- Country ---
class CountryListAPIView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.AllowAny]


# --- Region ---
class RegionListAPIView(generics.ListAPIView):
    queryset = Region.objects.select_related('country').all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.AllowAny]


# --- District ---
class DistrictListAPIView(generics.ListAPIView):
    queryset = District.objects.select_related('region__country').all()
    serializer_class = DistrictSerializer
    permission_classes = [permissions.AllowAny]
