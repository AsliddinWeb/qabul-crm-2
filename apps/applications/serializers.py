from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    program_name = serializers.CharField(source='program.name', read_only=True)
    contract_file_url = serializers.FileField(source='contract_file', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'user',
            'user_full_name',
            'reviewed_by',
            'admission_type',
            'branch',
            'education_level',
            'education_form',
            'program',
            'program_name',
            'diplom',
            'transfer_diplom',
            'course',
            'contract_file',
            'contract_file_url',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['status', 'created_at', 'updated_at', 'user', 'reviewed_by', 'course']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and hasattr(request, 'user') and request.user.is_authenticated:
            # Telegram foydalanuvchisining diplom fayllarini topshirishini talab qilmaslik
            if hasattr(request.user, 'telegram_id') and request.user.telegram_id:
                self.fields['diplom'].required = False
                self.fields['transfer_diplom'].required = False
            else:
                self.fields['diplom'].required = True
                if self.initial_data.get('admission_type') == 'transfer':
                    self.fields['transfer_diplom'].required = True

