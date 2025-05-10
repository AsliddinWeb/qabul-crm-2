from django.db import models
from django.conf import settings
from apps.regions.models import Country, Region, District


class EducationType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class InstitutionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Diplom(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diplom')
    serial_number = models.CharField(max_length=100)
    education_type = models.ForeignKey(EducationType, on_delete=models.CASCADE)
    institution_type = models.ForeignKey(InstitutionType, on_delete=models.CASCADE)

    university_name = models.TextField()
    graduation_year = models.CharField(max_length=4)

    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    diploma_file = models.FileField(upload_to='diploms/')

    def __str__(self):
        return self.serial_number


class TransferDiplom(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transfer_diplom')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    university_name = models.TextField()
    target_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    transcript_file = models.FileField(upload_to='transcripts/')

    def __str__(self):
        return self.university_name
