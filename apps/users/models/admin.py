from django.conf import settings
from django.db import models
from apps.users.models import User


class Admin(User):
    class Meta:
        proxy = True
        verbose_name = 'Administrator'
        verbose_name_plural = 'Administratorlar'

    def save(self, *args, **kwargs):
        self.role = 'ADMIN'
        super().save(*args, **kwargs)


class AdminProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_profile',
        limit_choices_to={'role': 'ADMIN'},
        verbose_name='Foydalanuvchi'
    )
    image = models.ImageField(
        upload_to='users/admins/photos/',
        blank=True,
        null=True,
        verbose_name='Rasm'
    )

    def __str__(self):
        return str(self.user.id)

    class Meta:
        verbose_name = 'Administrator profili'
        verbose_name_plural = 'Administrator profillari'
