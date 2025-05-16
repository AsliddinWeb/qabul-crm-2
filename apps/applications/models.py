from django.db import models
from django.conf import settings
from apps.programs.models import Branch, EducationForm, Program, EducationLevel
from apps.diploms.models import Diplom, TransferDiplom, Course


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Yuborilgan'),
        ('review', 'Ko‘rib chiqilmoqda'),
        ('accepted', 'Qabul qilindi'),
        ('rejected', 'Rad etildi'),
    ]

    ADMISSION_TYPE_CHOICES = [
        ('regular', '1-kurs (Yangi qabul)'),
        ('transfer', 'Perevod (O‘qishni ko‘chirish)'),
    ]

    # Faqat Applicant foydalanuvchilar
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'APPLICANT'},
        verbose_name="Foydalanuvchi"
    )

    # Staff tomonidan biriktiriladigan xodim (ko‘rib chiqish uchun)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications',
        verbose_name="Ko‘rib chiquvchi xodim"
    )

    admission_type = models.CharField(
        max_length=20,
        choices=ADMISSION_TYPE_CHOICES,
        default='regular',
        verbose_name="Qabul turi"
    )

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="Filial")
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, verbose_name="Taʼlim darajasi")
    education_form = models.ForeignKey(EducationForm, on_delete=models.CASCADE, verbose_name="Taʼlim shakli")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name="Yo‘nalish")

    diplom = models.ForeignKey(Diplom, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Diplom")
    transfer_diplom = models.ForeignKey(TransferDiplom, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Perevod diplomi")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kurs")

    contract_file = models.FileField(
        upload_to='contracts/',
        null=True,
        blank=True,
        verbose_name="Shartnoma fayli"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Holati"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O‘zgartirilgan sana")

    def __str__(self):
        return f"{self.user.full_name or self.user.phone} - {self.program.name} ({self.get_admission_type_display()})"

    class Meta:
        verbose_name = "Ariza"
        verbose_name_plural = "Barcha Arizalar"
