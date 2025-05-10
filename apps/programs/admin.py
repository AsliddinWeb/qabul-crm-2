from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Branch, EducationLevel, EducationForm, Program


@admin.register(Branch)
class BranchAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)


@admin.register(EducationLevel)
class EducationLevelAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)


@admin.register(EducationForm)
class EducationFormAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)


@admin.register(Program)
class ProgramAdmin(ModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'id', 'code', 'branch', 'education_level', 'education_form', 'tuition_fee')
    list_filter = ('branch', 'education_level', 'education_form')
    search_fields = ('name', 'code', 'tuition_fee', 'study_duration', 'contract_series')
    ordering = ('id',)
