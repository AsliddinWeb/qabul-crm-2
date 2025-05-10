from django.contrib import admin, messages
from django.contrib.admin import DateFieldListFilter, SimpleListFilter
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import path
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.core.files.base import ContentFile
from django.utils.text import slugify

from weasyprint import HTML
from io import BytesIO

from unfold.admin import ModelAdmin as UnfoldModelAdmin  # 🔹 Unfolddan foydalaniladi

from apps.users.models import User
from .models import Application
from .forms import ApplicationAdminForm


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
class ApplicationAdmin(UnfoldModelAdmin):  # 🔹 UnfoldModelAdmin ishlatilmoqda
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
    change_form_template = 'admin/application_change_form.html'  # 🔹 agar kerakli o‘zgartirishlar bo‘lsa

    search_fields = ('user__full_name', 'user__phone')
    readonly_fields = ('reviewed_by', 'contract_file', 'course', 'telegram_info')

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
        html_string = render_to_string("contracts/contract_template.html", {'application': application})
        html = HTML(string=html_string)
        pdf_file = BytesIO()
        html.write_pdf(target=pdf_file)
        pdf_file.seek(0)
        filename = f"shartnoma_{slugify(application.user.full_name or application.user.phone)}.pdf"
        application.contract_file.save(filename, ContentFile(pdf_file.read()))
        application.save()
        self.message_user(request, "📄 Shartnoma PDF generatsiya qilindi.")
        return redirect(f"../../{object_id}/change/")

    def user_has_telegram(self, obj):
        return bool(obj.user.telegram_id)
    user_has_telegram.boolean = True
    user_has_telegram.short_description = "Telegram ID"

    def telegram_info(self, obj):
        if obj.user and obj.user.telegram_id:
            return format_html(
                "<b>Telegram ID:</b> <code>{}</code><br><span style='color:green;'>Telegramdan kelgan.</span>",
                obj.user.telegram_id
            )
        return mark_safe("<span style='color:red;'>Telegram ID mavjud emas</span>")
    telegram_info.short_description = "Telegram ma’lumot"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'reviewed_by':
            kwargs["queryset"] = User.objects.filter(role__in=['STAFF', 'ADMIN'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.reviewed_by and request.user.role in ['STAFF', 'ADMIN']:
            obj.reviewed_by = request.user
        elif not obj.reviewed_by:
            messages.warning(request, "Faqat STAFF yoki ADMIN foydalanuvchilar reviewed_by bo‘la oladi.")
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields if obj else self.readonly_fields
