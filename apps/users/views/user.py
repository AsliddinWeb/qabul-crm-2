from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

from apps.diploms.serializers import DiplomCreateSerializer, TransferDiplomCreateSerializer
from apps.applications.models import Application
from apps.applications.serializers import ApplicationSerializer as ApplicationCreateSerializer



# Swagger Docs
from drf_yasg.utils import swagger_auto_schema

from apps.users.serializers import (
    VerifyCodeSerializer,
    PasswordResetSendCodeSerializer,
    PasswordResetConfirmSerializer, 
    CombinedAuthSerializer,
    ApplicantProfileCreateSerializer,
    ApplicantCreateByStaffSerializer
)

from apps.users.permissions import IsStaffOrAdmin


class CombinedAuthView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CombinedAuthSerializer

    @swagger_auto_schema(tags=["auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# class RegisterView(generics.CreateAPIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = RegisterSerializer

#     @swagger_auto_schema(tags=["auth"])
#     def post(self, request, *args, **kwargs):
#         return super().post(request, *args, **kwargs)


class VerifyCodeView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifyCodeSerializer

    @swagger_auto_schema(tags=["auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# class LoginView(generics.CreateAPIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = LoginSerializer

#     @swagger_auto_schema(tags=["auth"])
#     def post(self, request, *args, **kwargs):
#         return super().post(request, *args, **kwargs)


class PasswordResetSendCodeView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetSendCodeSerializer

    @swagger_auto_schema(tags=["auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PasswordResetConfirmView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    @swagger_auto_schema(tags=["auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["auth"])
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Tizimdan chiqildi."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Token noto‘g‘ri yoki bekor qilib bo‘lmadi."}, status=status.HTTP_400_BAD_REQUEST)


class ApplicantProfileCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplicantProfileCreateSerializer

    @swagger_auto_schema(tags=["auth"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CreateApplicantByStaffView(generics.CreateAPIView):
    serializer_class = ApplicantCreateByStaffSerializer
    permission_classes = [IsAuthenticated, IsStaffOrAdmin]


class GetMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # --- Bog‘langan ma’lumotlar
        applicant_profile = None
        diplom = None
        transfer_diplom = None
        application = None

        if hasattr(user, 'applicant_profile'):
            applicant_profile = ApplicantProfileCreateSerializer(user.applicant_profile).data

        if hasattr(user, 'diploma'):
            diplom = DiplomCreateSerializer(user.diploma).data

        if hasattr(user, 'transfer_diploma'):
            transfer_diplom = TransferDiplomCreateSerializer(user.transfer_diploma).data

        try:
            application = Application.objects.get(user=user)
            application = ApplicationCreateSerializer(application).data
        except Application.DoesNotExist:
            application = None

        return Response({
            "id": user.id,
            "phone": user.phone,
            "telegram_id": user.telegram_id,
            "role": user.role,
            "is_verified": user.is_verified,
            "full_name": user.full_name,
            "profile": applicant_profile,
            "diplom": diplom,
            "transfer_diplom": transfer_diplom,
            "application": application
        })
