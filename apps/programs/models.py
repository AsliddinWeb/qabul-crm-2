from django.db import models


class Branch(models.Model):
    """University branches like: Tashkent, Andijan, Nukus"""
    name = models.CharField(max_length=100, verbose_name="Filial nomi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Filial"
        verbose_name_plural = "Filiallar"


class EducationLevel(models.Model):
    """Education level: Bachelor, Master, etc."""
    name = models.CharField(max_length=100, verbose_name="Taʼlim darajasi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Taʼlim darajasi"
        verbose_name_plural = "Taʼlim darajalari"


class EducationForm(models.Model):
    """Education form: Full-time, Part-time, Evening"""
    name = models.CharField(max_length=100, verbose_name="Taʼlim shakli")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Taʼlim shakli"
        verbose_name_plural = "Taʼlim shakllari"


class Program(models.Model):
    """Educational programs: direction, tuition fee, duration, etc."""
    image = models.ImageField(upload_to='programs/program/', null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name="Yo‘nalish nomi")
    code = models.CharField(max_length=100, verbose_name="Yo‘nalish kodi")

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="Filial")
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, verbose_name="Taʼlim darajasi")
    education_form = models.ForeignKey(EducationForm, on_delete=models.CASCADE, verbose_name="Taʼlim shakli")

    tuition_fee = models.CharField(max_length=255, verbose_name="Kontrakt summasi")
    study_duration = models.CharField(max_length=100, verbose_name="O‘qish muddati")
    contract_series = models.CharField(max_length=100, verbose_name="Shartnoma seriyasi")

    def __str__(self):
        return f"{self.name} - ({self.education_form}) - ({self.education_level})"

    class Meta:
        verbose_name = "Yo‘nalish"
        verbose_name_plural = "Yo‘nalishlar"
