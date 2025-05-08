from django.contrib import admin
from django.contrib import messages

from apps.users.models import User
from .models import Application
from .forms import ApplicationAdminForm


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationAdminForm
    
    list_display = (
        'user', 'program', 'admission_type', 'status',
        'reviewed_by', 'created_at'
    )
    list_filter = ('status', 'admission_type', 'branch', 'education_level')
    search_fields = ('user__full_name', 'user__phone')

    readonly_fields = ('reviewed_by', 'contract_file', 'course')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Only STAFF and ADMIN can be shown in reviewed_by
        if db_field.name == 'reviewed_by':
            kwargs["queryset"] = User.objects.filter(role__in=['STAFF', 'ADMIN'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.reviewed_by:
            if request.user.role in ['STAFF', 'ADMIN']:
                obj.reviewed_by = request.user
            else:
                messages.warning(request, "Faqat STAFF yoki ADMIN foydalanuvchilar reviewed_by bo‘la oladi.")
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """
        readonly_fields may vary — new entries allow all, existing entries lock reviewed_by & contract_file
        """
        if obj:  # existing object
            return self.readonly_fields
        return self.readonly_fields
