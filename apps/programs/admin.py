from django.contrib import admin
from .models import Branch, EducationLevel, EducationForm, Program


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(EducationForm)
class EducationFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'branch', 'education_level', 'education_form', 'tuition_fee')
    list_filter = ('branch', 'education_level', 'education_form')
    search_fields = ('name', 'code', 'tuition_fee', 'study_duration', 'contract_series')
    ordering = ('id',)
