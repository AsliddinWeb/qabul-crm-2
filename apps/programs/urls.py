from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.programs.views import (
    BranchViewSet, EducationLevelViewSet,
    EducationFormViewSet, ProgramViewSet
)

router = DefaultRouter()
router.register(r'branches', BranchViewSet, basename='branches')
router.register(r'education-levels', EducationLevelViewSet, basename='education-levels')
router.register(r'education-forms', EducationFormViewSet, basename='education-forms')
router.register(r'programs', ProgramViewSet, basename='programs')

urlpatterns = [
    path('', include(router.urls)),
]
