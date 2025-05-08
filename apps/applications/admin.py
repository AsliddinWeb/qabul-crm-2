from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter, SimpleListFilter
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.users.models import User
from .models import Application
from .forms import ApplicationAdminForm

# Contract PDF
from django.urls import path
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.text import slugify


# 🔷 Telegram ID bo‘yicha filter
class TelegramIDFilter(SimpleListFilter):
    title = 'By Telegram ID'
    parameter_name = 'has_telegram'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Telegram ID mavjud'),
            ('no', 'Telegram ID yo‘q'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(user__telegram_id__isnull=False).exclude(user__telegram_id='')
        elif self.value() == 'no':
            return queryset.filter(user__telegram_id__isnull=True) | queryset.filter(user__telegram_id='')
        return queryset


# 🔷 Faqat STAFF va ADMIN roldagi `reviewed_by` filteri
class ReviewedByStaffOrAdminFilter(SimpleListFilter):
    title = "Reviewed by"
    parameter_name = "reviewed_by"

    def lookups(self, request, model_admin):
        users = User.objects.filter(role__in=['STAFF', 'ADMIN'])
        return [(user.id, f"{user.phone} ({user.role})") for user in users]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(reviewed_by__id=self.value())
        return queryset


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationAdminForm

    list_display = (
        'user',
        'user_has_telegram',
        'program',
        'admission_type',
        'status',
        'reviewed_by',
        'created_at',
    )

    list_filter = (
        'status',
        'admission_type',
        'branch',
        'education_level',
        'education_form',
        'program',
        ('created_at', DateFieldListFilter),
        'user__is_verified',
        TelegramIDFilter,
        ReviewedByStaffOrAdminFilter,
    )

    ordering = ('-updated_at',)
    change_form_template = 'admin/application_change_form.html'

    search_fields = ('user__full_name', 'user__phone')
    readonly_fields = ('reviewed_by', 'contract_file', 'course', 'telegram_info')

    # Contract
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/generate-contract/',
                self.admin_site.admin_view(self.generate_contract),
                name='generate_contract',
            ),
        ]
        return custom_urls + urls

    def generate_contract(self, request, object_id):
        application = self.get_object(request, object_id)

        # 1. HTML shablonni yuklash
        html_string = render_to_string("contracts/contract_template.html", {
            'application': application,
        })

        # 2. WeasyPrint orqali PDF generatsiya qilish
        html = HTML(string=html_string)
        pdf_file = BytesIO()
        html.write_pdf(target=pdf_file)
        pdf_file.seek(0)

        # 3. Fayl nomi va saqlash
        filename = f"shartnoma_{slugify(application.user.full_name or application.user.phone)}.pdf"
        application.contract_file.save(filename, ContentFile(pdf_file.read()))
        application.save()

        # 4. Admin sahifasiga qaytarish
        self.message_user(request, "📄 Shartnoma PDF generatsiya qilindi.")
        return redirect(f"../../{object_id}/change/")

    # 🔹 Telegram ID mavjudligini boolean ko‘rinishda chiqarish
    def user_has_telegram(self, obj):
        return bool(obj.user.telegram_id)
    user_has_telegram.boolean = True
    user_has_telegram.short_description = "Telegram ID"

    # 🔹 Telegram ID’ni admin formda ko‘rsatish (readonly_info)
    def telegram_info(self, obj):
        if obj.user and obj.user.telegram_id:
            return format_html(
                "<b>Telegram ID:</b> <code>{}</code><br><span style='color:green;'>Telegramdan kelgan.</span>",
                obj.user.telegram_id
            )
        return mark_safe("<span style='color:red;'>Telegram ID mavjud emas</span>")
    telegram_info.short_description = "Telegram ma’lumot"

    # 🔹 reviewed_by uchun faqat STAFF va ADMIN ko‘rsatish
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'reviewed_by':
            kwargs["queryset"] = User.objects.filter(role__in=['STAFF', 'ADMIN'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # 🔹 reviewed_by ni avtomatik to‘ldirish
    def save_model(self, request, obj, form, change):
        if not obj.reviewed_by and request.user.role in ['STAFF', 'ADMIN']:
            obj.reviewed_by = request.user
        elif not obj.reviewed_by:
            messages.warning(request, "Faqat STAFF yoki ADMIN foydalanuvchilar reviewed_by bo‘la oladi.")
        super().save_model(request, obj, form, change)

    # 🔹 readonly_fields dinamik boshqaruv
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields if obj else self.readonly_fields
