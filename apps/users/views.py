from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


# Swagger Docs
from drf_yasg.utils import swagger_auto_schema

from .serializers import (
    VerifyCodeSerializer,
    PasswordResetSendCodeSerializer,
    PasswordResetConfirmSerializer, 
    CombinedAuthSerializer,
    ApplicantProfileCreateSerializer
)


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
