from django.db import models
from django.conf import settings
from apps.programs.models import Branch, EducationForm, Program, EducationLevel
from apps.diploms.models import Diplom, TransferDiplom, Course


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Submitted'),
        ('review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    ADMISSION_TYPE_CHOICES = [
        ('regular', '1st Year (New Admission)'),
        ('transfer', 'Transfer (Perevod)'),
    ]

    # Faqat Applicant foydalanuvchilar
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'APPLICANT'}
    )

    # Staff tomonidan biriktiriladigan xodim (ko‘rib chiqish uchun)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications'
    )

    admission_type = models.CharField(max_length=20, choices=ADMISSION_TYPE_CHOICES, default='regular')

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    education_level = models.ForeignKey(EducationLevel, on_delete=models.CASCADE)
    education_form = models.ForeignKey(EducationForm, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    diplom = models.ForeignKey(Diplom, on_delete=models.SET_NULL, null=True, blank=True)
    transfer_diplom = models.ForeignKey(TransferDiplom, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

    # Staff tomonidan yuklanadigan shartnoma fayli
    contract_file = models.FileField(upload_to='contracts/', null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name or self.user.phone} - {self.program.name} ({self.get_admission_type_display()})"
