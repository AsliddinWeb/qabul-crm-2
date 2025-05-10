from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Country, Region, District


# --- Inline Admins ---
class RegionInline(TabularInline):
    model = Region
    extra = 0


class DistrictInline(TabularInline):
    model = District
    extra = 0


# --- Country Admin ---
@admin.register(Country)
class CountryAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
    inlines = [RegionInline]


# --- Region Admin ---
@admin.register(Region)
class RegionAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'id', 'country')
    search_fields = ('name',)
    list_filter = ('country',)
    inlines = [DistrictInline]


# --- District Admin ---
@admin.register(District)
class DistrictAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'id', 'region')
    search_fields = ('name',)
    list_filter = ('region__country', 'region')
