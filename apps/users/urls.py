from django.urls import path
from .views import (
    VerifyCodeView, 
    LogoutView, PasswordResetSendCodeView, PasswordResetConfirmView, 
    ApplicantProfileCreateView, CombinedAuthView, CreateApplicantByStaffView, GetPassportInfoFromGov
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', CombinedAuthView.as_view(), name='combined_auth'),  # 🔥 login/register birgalikda
    # path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyCodeView.as_view(), name='verify'),
    # path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('password/send-code/', PasswordResetSendCodeView.as_view(), name='password_send_code'),
    path('password/reset/', PasswordResetConfirmView.as_view(), name='password_reset'),

    path('profile/create/', ApplicantProfileCreateView.as_view(), name='applicant_profile_create'),

    # Staff
    path('staff-create/', CreateApplicantByStaffView.as_view(), name='staff_create_applicant'),

    # Get Passport Info
    path('get-passport-info/', GetPassportInfoFromGov.as_view(), name='passport-info-from-gov'),
]
