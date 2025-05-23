from django.db import models
from django.conf import settings

from apps.users.models import User


class Staff(User):
    class Meta:
        proxy = True
        verbose_name = 'Xodim'
        verbose_name_plural = 'Xodimlar'

    def save(self, *args, **kwargs):
        self.role = 'STAFF'
        super().save(*args, **kwargs)


class StaffProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile',
        limit_choices_to={'role': 'STAFF'},
        verbose_name='Foydalanuvchi'
    )
    position = models.CharField("Lavozimi", max_length=100, null=True, blank=True)
    image = models.ImageField("Rasm", upload_to='users/staffs/photos/', blank=True, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Xodim profili'
        verbose_name_plural = 'Xodim profillari'
