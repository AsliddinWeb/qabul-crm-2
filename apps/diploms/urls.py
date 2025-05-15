# urls.py
from django.urls import path
from .views import (
    DiplomCreateView, TransferDiplomCreateView,
    DiplomStaffCreateView, TransferDiplomStaffCreateView,
    DiplomDetailView, TransferDiplomDetailView, EducationTypeListView, InstitutionTypeListView, CourseListView
)

urlpatterns = [
    # Applicant
    path('diplom/create/', DiplomCreateView.as_view(), name='diplom-create'),
    path('transfer-diplom/create/', TransferDiplomCreateView.as_view(), name='transfer-diplom-create'),

    # Staff/Admin
    path('staff/diplom/create/', DiplomStaffCreateView.as_view(), name='staff-diplom-create'),
    path('staff/transfer-diplom/create/', TransferDiplomStaffCreateView.as_view(), name='staff-transfer-diplom-create'),

    # Check existence
    path('diplom/', DiplomDetailView.as_view(), name='diplom-detail'),
    path('transfer-diplom/', TransferDiplomDetailView.as_view(), name='transfer-diplom-detail'),

    # Diplom APIs
    path('education-types/', EducationTypeListView.as_view(), name='education-type-list'),
    path('institution-types/', InstitutionTypeListView.as_view(), name='institution-type-list'),
    path('courses/', CourseListView.as_view(), name='course-list'),
]
