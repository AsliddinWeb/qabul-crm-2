from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema

from apps.programs.models import Branch, EducationLevel, EducationForm, Program
from apps.programs.serializers import (
    BranchSerializer, EducationLevelSerializer, EducationFormSerializer, ProgramSerializer
)


class BranchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_summary="Filiallar ro‘yxatini olish")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Bitta filial haqida ma’lumot")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class EducationLevelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_summary="Ta’lim darajalari ro‘yxatini olish")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Bitta ta’lim darajasi haqida ma’lumot")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class EducationFormViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EducationForm.objects.all()
    serializer_class = EducationFormSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_summary="Ta’lim shakllari ro‘yxatini olish")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Bitta ta’lim shakli haqida ma’lumot")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Program.objects.select_related('branch', 'education_level', 'education_form').all()
    serializer_class = ProgramSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['branch', 'education_level', 'education_form']

    @swagger_auto_schema(operation_summary="Yo‘nalishlar ro‘yxatini olish (filter bilan)")
    def list(self, request, *args, **kwargs):
        """
        Branch, education_level va education_form bo‘yicha filterlash imkoniyati mavjud:
        - ?branch=1
        - ?education_level=2
        - ?education_form=3
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Bitta yo‘nalish haqida ma’lumot")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)