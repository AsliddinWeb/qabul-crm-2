from django.db import models


class Branch(models.Model):
    """University branches like: Tashkent, Andijan, Nukus"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EducationLevel(models.Model):
    """Education level: Bachelor, Master, etc."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EducationForm(models.Model):
    """Education form: Full-time, Part-time, Evening"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Program(models.Model):
    """Educational programs: direction, tuition fee, duration, etc."""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE)
    education_form = models.ForeignKey(EducationForm, on_delete=models.CASCADE)

    tuition_fee = models.CharField(max_length=255)
    study_duration = models.CharField(max_length=100)
    contract_series = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - ({self.education_form}) - ({self.education_level})"
