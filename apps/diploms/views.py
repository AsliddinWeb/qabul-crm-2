# views.py
from rest_framework import generics, permissions
from apps.diploms.models import Diplom, TransferDiplom
from apps.diploms.serializers import (
    DiplomCreateSerializer, TransferDiplomCreateSerializer,
    DiplomStaffCreateSerializer, TransferDiplomStaffCreateSerializer,
    DiplomExistSerializer, TransferDiplomExistSerializer
)


# --- User (Applicant) uchun create ---
class DiplomCreateView(generics.CreateAPIView):
    serializer_class = DiplomCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransferDiplomCreateView(generics.CreateAPIView):
    serializer_class = TransferDiplomCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


# --- STAFF yoki ADMIN uchun boshqa foydalanuvchi uchun create ---
class DiplomStaffCreateView(generics.CreateAPIView):
    serializer_class = DiplomStaffCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class TransferDiplomStaffCreateView(generics.CreateAPIView):
    serializer_class = TransferDiplomStaffCreateSerializer
    permission_classes = [permissions.IsAdminUser]


# --- Diplom borligini tekshirish va olish ---
class DiplomDetailView(generics.RetrieveAPIView):
    serializer_class = DiplomExistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.diplom


class TransferDiplomDetailView(generics.RetrieveAPIView):
    serializer_class = TransferDiplomExistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.transfer_diplom
