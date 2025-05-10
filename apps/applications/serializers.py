from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.applications.models import Application

User = get_user_model()


# --- Applicant (oddiy foydalanuvchi) uchun ariza yaratish ---
class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        exclude = ('reviewed_by', 'contract_file', 'course', 'status')

    def validate(self, attrs):
        user = self.context['request'].user
        if Application.objects.filter(user=user).exists():
            raise serializers.ValidationError("❌ Siz allaqachon ariza topshirgansiz.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return Application.objects.create(user=user, **validated_data)


# --- Staff/Admin tomonidan ariza yaratish ---
class ApplicationStaffCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)

    class Meta:
        model = Application
        exclude = ('user', 'reviewed_by', 'contract_file', 'course', 'status')

    def validate_phone(self, value):
        try:
            user = User.objects.get(phone=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("❌ Bunday foydalanuvchi mavjud emas.")
        if Application.objects.filter(user=user).exists():
            raise serializers.ValidationError("❌ Bu foydalanuvchi allaqachon ariza topshirgan.")
        self.context['target_user'] = user  # saqlab qo'yamiz
        return value

    def create(self, validated_data):
        user = self.context['target_user']
        validated_data.pop('phone')  # phone ni olib tashlaymiz
        return Application.objects.create(user=user, **validated_data)
