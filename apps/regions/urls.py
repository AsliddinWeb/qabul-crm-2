from django.urls import path
from .views import CountryListAPIView, RegionListAPIView, DistrictListAPIView

urlpatterns = [
    path('countries/', CountryListAPIView.as_view(), name='country-list'),
    path('regions/', RegionListAPIView.as_view(), name='region-list'),
    path('districts/', DistrictListAPIView.as_view(), name='district-list'),
]
