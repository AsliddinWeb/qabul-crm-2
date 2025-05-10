from django.db import models
from django.conf import settings

from apps.users.models import User
from apps.regions.models import Country, Region, District

class Applicant(User):
    class Meta:
        proxy = True
        verbose_name = 'Abituriyent'
        verbose_name_plural = 'Abituriyentlar'

    def save(self, *args, **kwargs):
        self.role = 'APPLICANT'
        super().save(*args, **kwargs)


class ApplicantProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applicant_profile',
        limit_choices_to={'role': 'APPLICANT'}
    )
    # full_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    other_name = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField()
    passport_series = models.CharField(max_length=50)
    pinfl = models.CharField(max_length=255)

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    gender = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)

    image = models.ImageField(upload_to='users/passports/images/', null=True, blank=True)
    passport_file = models.FileField(upload_to='users/passports/files/', null=True, blank=True)

    def __str__(self):
        return f"{self.last_name or ''} {self.first_name or ''} {self.other_name or ''}".strip()

