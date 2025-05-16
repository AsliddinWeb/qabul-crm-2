from django.db import models
from django.conf import settings
from apps.regions.models import Country, Region, District


class EducationType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Taʼlim turi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Taʼlim turi"
        verbose_name_plural = "Taʼlim turlari"


class InstitutionType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Muassasa turi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Muassasa turi"
        verbose_name_plural = "Muassasa turlari"


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kurs")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"


class Diplom(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='diplom',
        verbose_name="Foydalanuvchi"
    )
    serial_number = models.CharField(max_length=100, verbose_name="Diplom raqami")
    education_type = models.ForeignKey(EducationType, on_delete=models.CASCADE, verbose_name="Taʼlim turi")
    institution_type = models.ForeignKey(InstitutionType, on_delete=models.CASCADE, verbose_name="Muassasa turi")

    university_name = models.TextField(verbose_name="Universitet nomi")
    graduation_year = models.CharField(max_length=4, verbose_name="Bitirgan yil")

    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Viloyat")
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Tuman")

    diploma_file = models.FileField(upload_to='diploms/', verbose_name="Diplom fayli")

    def __str__(self):
        return self.serial_number

    class Meta:
        verbose_name = "Diplom"
        verbose_name_plural = "Diplomlar"


class TransferDiplom(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transfer_diplom',
        verbose_name="Foydalanuvchi"
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Davlat")
    university_name = models.TextField(verbose_name="Universitet nomi")
    target_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")
    transcript_file = models.FileField(upload_to='transcripts/', verbose_name="Transcript fayli")

    def __str__(self):
        return self.university_name

    class Meta:
        verbose_name = "Perevod diplomi"
        verbose_name_plural = "Perevod diplomlari"
