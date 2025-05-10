from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.applications.models import Application
from apps.applications.serializers import (
    ApplicationCreateSerializer,
    ApplicationStaffCreateSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


# --- Applicant uchun: o‘z arizasini yaratish/ko‘rish ---
class ApplicationMeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="O‘zi topshirgan arizani ko‘rish",
        responses={
            200: ApplicationCreateSerializer(),
            404: 'Siz hali ariza topshirmagansiz.'
        }
    )
    def get(self, request):
        try:
            application = Application.objects.get(user=request.user)
            serializer = ApplicationCreateSerializer(application)
            return Response(serializer.data)
        except Application.DoesNotExist:
            return Response({"detail": "Siz hali ariza topshirmagansiz."}, status=404)

    @swagger_auto_schema(
        operation_summary="Yangi ariza topshirish (Foydalanuvchi)",
        request_body=ApplicationCreateSerializer,
        responses={
            201: ApplicationCreateSerializer(),
            400: 'Yaroqsiz maʼlumotlar'
        }
    )
    def post(self, request):
        serializer = ApplicationCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            return Response(ApplicationCreateSerializer(instance).data, status=201)
        return Response(serializer.errors, status=400)


# --- Staff yoki Admin uchun: telefon raqam orqali boshqa foydalanuvchiga ariza kiritish ---
class ApplicationByPhoneView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Telefon raqam orqali arizani ko‘rish (Admin/Staff)",
        manual_parameters=[
            openapi.Parameter(
                'phone', openapi.IN_QUERY, description="Foydalanuvchi telefon raqami (masalan: +998901234567)",
                type=openapi.TYPE_STRING, required=True
            )
        ],
        responses={
            200: ApplicationCreateSerializer(),
            404: "Foydalanuvchi yoki ariza topilmadi",
            400: "Telefon raqam yuboring"
        }
    )
    def get(self, request):
        phone = request.query_params.get('phone')
        if not phone:
            return Response({"detail": "Telefon raqam yuboring."}, status=400)
        try:
            user = User.objects.get(phone=phone)
            application = Application.objects.get(user=user)
            return Response(ApplicationCreateSerializer(application).data)
        except User.DoesNotExist:
            return Response({"detail": "Bunday foydalanuvchi topilmadi."}, status=404)
        except Application.DoesNotExist:
            return Response({"detail": "Bu foydalanuvchi hali ariza topshirmagan."}, status=404)

    @swagger_auto_schema(
        operation_summary="Yangi ariza qo‘shish (Admin/Staff)",
        request_body=ApplicationStaffCreateSerializer,
        responses={
            201: ApplicationCreateSerializer(),
            400: 'Yaroqsiz maʼlumot'
        }
    )
    def post(self, request):
        serializer = ApplicationStaffCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            return Response(ApplicationCreateSerializer(instance).data, status=201)
        return Response(serializer.errors, status=400)
