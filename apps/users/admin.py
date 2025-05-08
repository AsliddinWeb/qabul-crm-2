from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models import (
    User, PhoneVerification,
    Applicant, Staff, Admin,
    ApplicantProfile, StaffProfile, AdminProfile
)

# --- Inline Profile Admins ---
class ApplicantProfileInline(admin.StackedInline):
    model = ApplicantProfile
    extra = 0
    can_delete = False


class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    extra = 0
    can_delete = False


class AdminProfileInline(admin.StackedInline):
    model = AdminProfile
    extra = 0
    can_delete = False


# --- Custom User Admin ---
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'phone', 'full_name', 'telegram_id', 'role', 'is_verified', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'is_verified')
    search_fields = ('phone', 'full_name', 'telegram_id')
    ordering = ('-id',)
    readonly_fields = ('last_login', 'is_verified')

    fieldsets = (
        (_('Login maʼlumotlari'), {
            'fields': ('phone', 'password')
        }),
        (_('Shaxsiy maʼlumotlar'), {
            'fields': ('full_name', 'telegram_id')
        }),
        (_('Ruxsatlar'), {
            'fields': ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Tizim maʼlumotlari'), {
            'fields': ('last_login',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'role', 'is_verified', 'is_active', 'is_staff', 'telegram_id')}
        ),
    )


# --- Proxy Model Admins ---
@admin.register(Applicant)
class ApplicantAdmin(UserAdmin):
    inlines = [ApplicantProfileInline]
    list_display = UserAdmin.list_display
    ordering = ('-id',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='APPLICANT')


@admin.register(Staff)
class StaffAdmin(UserAdmin):
    inlines = [StaffProfileInline]
    list_display = UserAdmin.list_display
    ordering = ('-id',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='STAFF')


@admin.register(Admin)
class AdminProxyAdmin(UserAdmin):
    inlines = [AdminProfileInline]
    list_display = UserAdmin.list_display
    ordering = ('-id',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role='ADMIN')


# --- Phone Verification Admin ---
@admin.register(PhoneVerification)
class PhoneVerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'code', 'created_at')
    search_fields = ('phone',)
    ordering = ('-id',)
    readonly_fields = ('created_at',)
