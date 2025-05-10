from rest_framework import serializers
from apps.programs.models import Branch, EducationLevel, EducationForm, Program


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = '__all__'


class EducationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationForm
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'
