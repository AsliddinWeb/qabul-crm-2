from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.utils import timezone
from datetime import timedelta

from apps.users.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("APPLICANT", "Ariza topshiruvchi"),
        ("STAFF", "Xodim"),
    )

    phone = models.CharField("Telefon raqam", max_length=20, unique=True)
    full_name = models.CharField("To‘liq ismi", max_length=255, blank=True, null=True)
    telegram_id = models.CharField("Telegram ID", max_length=255, null=True, blank=True)

    role = models.CharField("Rol", max_length=20, choices=ROLE_CHOICES, default='APPLICANT')

    is_active = models.BooleanField("Faolmi?", default=True)
    is_staff = models.BooleanField("Staff huquqi bormi?", default=False)
    is_verified = models.BooleanField("Tasdiqlanganmi?", default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return f"{self.full_name or self.phone} ({self.role})"

    @property
    def profile(self):
        if self.role == 'APPLICANT':
            return getattr(self, 'applicant_profile', None)
        elif self.role == 'STAFF':
            return getattr(self, 'staff_profile', None)
        elif self.role == 'ADMIN':
            return getattr(self, 'admin_profile', None)
        return None


class PhoneVerification(models.Model):
    phone = models.CharField("Telefon raqam", max_length=20)
    code = models.CharField("Tasdiqlash kodi", max_length=6)
    created_at = models.DateTimeField("Yaratilgan vaqti", auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=1)
    
    @classmethod
    def can_send_code(cls, phone):
        latest = cls.objects.filter(phone=phone).order_by('-created_at').first()
        if latest and not latest.is_expired():
            return False
        return True

    class Meta:
        verbose_name = "Telefonni tasdiqlash"
        verbose_name_plural = "Tasdiqlash kodlari"

    def __str__(self):
        return f"{self.phone} - {self.code}"
