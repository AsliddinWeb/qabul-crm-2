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
        limit_choices_to={'role': 'APPLICANT'},
        verbose_name='Foydalanuvchi'
    )
    last_name = models.CharField("Familiya", max_length=255, blank=True, null=True)
    first_name = models.CharField("Ism", max_length=255, blank=True, null=True)
    other_name = models.CharField("Otasining ismi", max_length=255, blank=True, null=True)
    birth_date = models.DateField("Tug‘ilgan sana")
    passport_series = models.CharField("Pasport seriyasi va raqami", max_length=50)
    pinfl = models.CharField("JShShIR (PINFL)", max_length=255)

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Davlat")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Viloyat")
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tuman")
    address = models.TextField("Yashash manzili", null=True, blank=True)

    gender = models.CharField("Jinsi", max_length=50, null=True, blank=True)
    nationality = models.CharField("Millati", max_length=50, null=True, blank=True)

    image = models.ImageField("Pasport rasmi", upload_to='users/passports/images/', null=True, blank=True)
    passport_file = models.FileField("Pasport fayli (PDF)", upload_to='users/passports/files/', null=True, blank=True)

    def __str__(self):
        return f"{self.last_name or ''} {self.first_name or ''} {self.other_name or ''}".strip()

    class Meta:
        verbose_name = 'Abituriyent profili'
        verbose_name_plural = 'Abituriyent profillari'
