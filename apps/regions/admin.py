from django.contrib import admin
from .models import Country, Region, District

class RegionInline(admin.TabularInline):
    model = Region
    extra = 0


class DistrictInline(admin.TabularInline):
    model = District
    extra = 0


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    inlines = [RegionInline]


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    search_fields = ('name',)
    list_filter = ('country',)
    inlines = [DistrictInline]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')
    search_fields = ('name',)
    list_filter = ('region__country', 'region')
