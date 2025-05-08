from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.utils import timezone
from datetime import timedelta

from apps.users.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("APPLICANT", "Applicant"),
        ("STAFF", "Staff"),
    )

    phone = models.CharField(max_length=20, unique=True)
    
    full_name = models.CharField(max_length=255, blank=True, null=True)
    telegram_id = models.CharField(max_length=255, null=True, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='APPLICANT')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.full_name or self.phone} ({self.role})"
    
    # 👇 Profile method
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
    phone = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=1)
    
    @classmethod
    def can_send_code(cls, phone):
        latest = cls.objects.filter(phone=phone).order_by('-created_at').first()
        if latest and not latest.is_expired():
            return False
        return True


    def __str__(self):
        return f"{self.phone} - {self.code}"

# class User(AbstractUser):
#     class Role(models.TextChoices):
#         ADMIN = "ADMIN", "Admin"
#         APPLICANT = "APPLICANT", "Applicant"
#         STAFF = "STAFF", "Staff"
    
#     phone = models.CharField(max_length=50, unique=True)
    
#     base_role = Role.APPLICANT

#     role = models.CharField(max_length=50, choices=Role.choices)

#     USERNAME_FIELD = 'phone'

#     def save(self, *arg, **kwargs):
#         if not self.pk:
#             self.role = self.base_role
#             return super().save(*arg, **kwargs)