from rest_framework import serializers
from apps.regions.models import Country, Region, District
from apps.diploms.models import Diplom, TransferDiplom, EducationType, InstitutionType, Course
from django.contrib.auth import get_user_model

User = get_user_model()


# --- Oddiy foydalanuvchi uchun Diplom create ---
class DiplomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diplom
        fields = [
            'serial_number', 'education_type', 'institution_type',
            'university_name', 'graduation_year',
            'region', 'district', 'diploma_file'
        ]

    def validate(self, attrs):
        user = self.context['request'].user
        if hasattr(user, 'diplom'):
            raise serializers.ValidationError("Ushbu foydalanuvchining diplomi allaqachon mavjud.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return Diplom.objects.create(user=user, **validated_data)


# --- Oddiy foydalanuvchi uchun TransferDiplom create ---
class TransferDiplomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferDiplom
        fields = ['country', 'university_name', 'target_course', 'transcript_file']

    def validate(self, attrs):
        user = self.context['request'].user
        if hasattr(user, 'transfer_diplom'):
            raise serializers.ValidationError("Transfer diplom allaqachon mavjud.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return TransferDiplom.objects.create(user=user, **validated_data)


# --- STAFF / ADMIN uchun Diplom yaratish ---
class DiplomStaffCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)

    class Meta:
        model = Diplom
        fields = [
            'phone', 'serial_number', 'education_type', 'institution_type',
            'university_name', 'graduation_year', 'region', 'district', 'diploma_file'
        ]

    def validate(self, attrs):
        phone = attrs.get('phone')
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError({"phone": "Bunday foydalanuvchi topilmadi."})
        if hasattr(user, 'diplom'):
            raise serializers.ValidationError("Bu foydalanuvchida allaqachon diplom mavjud.")
        self.user = user
        return attrs

    def create(self, validated_data):
        validated_data.pop('phone')
        return Diplom.objects.create(user=self.user, **validated_data)


# --- STAFF / ADMIN uchun TransferDiplom yaratish ---
class TransferDiplomStaffCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)

    class Meta:
        model = TransferDiplom
        fields = ['phone', 'country', 'university_name', 'target_course', 'transcript_file']

    def validate(self, attrs):
        phone = attrs.get('phone')
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError({"phone": "Bunday foydalanuvchi topilmadi."})
        if hasattr(user, 'transfer_diplom'):
            raise serializers.ValidationError("Bu foydalanuvchida allaqachon transfer diplom mavjud.")
        self.user = user
        return attrs

    def create(self, validated_data):
        validated_data.pop('phone')
        return TransferDiplom.objects.create(user=self.user, **validated_data)


class DiplomExistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diplom
        fields = '__all__'


class TransferDiplomExistSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferDiplom
        fields = '__all__'
