from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    EducationType,
    InstitutionType,
    Course,
    Diplom,
    TransferDiplom
)


@admin.register(EducationType)
class EducationTypeAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)


@admin.register(InstitutionType)
class InstitutionTypeAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)


@admin.register(Diplom)
class DiplomAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'id', 'serial_number', 'education_type', 'institution_type', 'graduation_year')
    search_fields = ('serial_number', 'user__phone', 'university_name')
    list_filter = ('education_type', 'institution_type', 'region', 'district')


@admin.register(TransferDiplom)
class TransferDiplomAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'id', 'university_name', 'country', 'target_course')
    search_fields = ('university_name', 'user__phone')
    list_filter = ('country', 'target_course')
