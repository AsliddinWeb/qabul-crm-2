from django.contrib import admin
from .models import (
    EducationType,
    InstitutionType,
    Course,
    Diplom,
    TransferDiplom
)


@admin.register(EducationType)
class EducationTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(InstitutionType)
class InstitutionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Diplom)
class DiplomAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'serial_number', 'education_type', 'institution_type', 'graduation_year')
    search_fields = ('serial_number', 'user__phone', 'university_name')
    list_filter = ('education_type', 'institution_type', 'region', 'district')


@admin.register(TransferDiplom)
class TransferDiplomAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'university_name', 'country', 'target_course')
    search_fields = ('university_name', 'user__phone')
    list_filter = ('country', 'target_course')
