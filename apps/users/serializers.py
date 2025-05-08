import random
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from apps.regions.models import Country, Region, District

from apps.users.models import PhoneVerification, ApplicantProfile
from .utils.eskiz import send_sms

User = get_user_model()

# --- Tasdiqlash kodi generator ---
def generate_code():
    return str(random.randint(1000, 9999))


# --- Yuborilgan kod muddati o‘tganini tekshirish ---
def can_send_code(phone):
    latest = PhoneVerification.objects.filter(phone=phone).order_by('-created_at').first()
    return not latest or latest.is_expired()


# --- Combined login/register ---
class CombinedAuthSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        if not value.startswith('998') or not value.isdigit():
            raise serializers.ValidationError("Telefon raqam noto‘g‘ri formatda.")
        return value

    def create(self, validated_data):
        phone = validated_data['phone']
        user, created = User.objects.get_or_create(phone=f"+{phone}", defaults={'is_verified': False})

        if not can_send_code(phone):
            raise serializers.ValidationError("Tasdiqlash kodi allaqachon yuborilgan. 1 daqiqa kuting.")

        code = generate_code()
        PhoneVerification.objects.create(phone=phone, code=code)
        send_sms(phone, f"Xalqaro innovatsion universiteti kodingiz: {code}")

        self.user = user
        self.created = created
        return user

    def to_representation(self, instance):
        return {
            "phone": instance.phone,
            "is_new": self.created,
            "is_verified": instance.is_verified,
            "detail": "Tasdiqlash kodi yuborildi."
        }


# --- Verify kodni tasdiqlash ---
class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['code']
        try:
            verification = PhoneVerification.objects.filter(phone=phone, code=code).latest('created_at')
        except PhoneVerification.DoesNotExist:
            raise serializers.ValidationError("Tasdiqlash kodi noto‘g‘ri.")
        if verification.is_expired():
            raise serializers.ValidationError("Kod eskirgan.")
        return attrs

    def create(self, validated_data):
        self.user = User.objects.get(phone=validated_data['phone'])
        self.user.is_verified = True
        self.user.save()
        return self.user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'phone': instance.phone,
            'is_verified': instance.is_verified,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


# --- Parol tiklash uchun kod yuborish ---
class PasswordResetSendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        if not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Bunday foydalanuvchi topilmadi.")
        return value

    def create(self, validated_data):
        phone = validated_data['phone']

        if not can_send_code(phone):
            raise serializers.ValidationError("Tasdiqlash kodi allaqachon yuborilgan. 1 daqiqa kuting.")

        code = generate_code()
        PhoneVerification.objects.create(phone=phone, code=code)
        send_sms(phone, f"Xalqaro innovatsion universiteti parolni tiklash kodingiz: {code}")
        user = User.objects.get(phone=phone)
        return user

    def to_representation(self, instance):
        return {
            "phone": instance.phone,
            "detail": "Tasdiqlash kodi yuborildi."
        }


# --- Parolni tiklashni tasdiqlash ---
class PasswordResetConfirmSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        phone = attrs['phone']
        code = attrs['code']
        try:
            verification = PhoneVerification.objects.filter(phone=phone, code=code).latest('created_at')
        except PhoneVerification.DoesNotExist:
            raise serializers.ValidationError("Kod noto‘g‘ri.")
        if verification.is_expired():
            raise serializers.ValidationError("Kod eskirgan.")
        return attrs

    def create(self, validated_data):
        user = User.objects.get(phone=validated_data['phone'])
        user.set_password(validated_data['new_password'])
        user.save()
        self.user = user
        return user

    def to_representation(self, instance):
        return {
            "phone": instance.phone,
            "detail": "Parol yangilandi."
        }


# --- Applicant profilini yaratish ---
class ApplicantProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantProfile
        fields = [
            'full_name', 'birth_date', 'passport_series', 'pinfl',
            'country', 'region', 'district', 'address',
            'gender', 'nationality', 'image', 'passport_file'
        ]

    def validate(self, attrs):
        user = self.context['request'].user
        if hasattr(user, 'applicant_profile'):
            raise serializers.ValidationError("Profil allaqachon yaratilgan.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        profile = ApplicantProfile.objects.create(user=user, **validated_data)
        return profile


class ApplicantCreateByStaffSerializer(serializers.ModelSerializer):
    # userga tegishli field
    phone = serializers.CharField()
    full_name = serializers.CharField()
    birth_date = serializers.DateField()
    passport_series = serializers.CharField()
    pinfl = serializers.CharField()
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=False)
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), required=False)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=False)
    address = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    nationality = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)
    passport_file = serializers.FileField(required=False)

    class Meta:
        model = ApplicantProfile
        fields = [
            'phone', 'full_name', 'birth_date', 'passport_series', 'pinfl',
            'country', 'region', 'district', 'address',
            'gender', 'nationality', 'image', 'passport_file'
        ]

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Bu telefon raqam bilan foydalanuvchi allaqachon mavjud.")
        return value

    def create(self, validated_data):
        # user uchun fieldlar
        phone = validated_data.pop('phone')
        full_name = validated_data.pop('full_name')

        # user yaratish
        user = User.objects.create(
            phone=phone,
            full_name=full_name,
            role='APPLICANT',
            is_verified=True,
        )

        # profile yaratish
        profile = ApplicantProfile.objects.create(user=user, **validated_data)
        return profile

    def to_representation(self, instance):
        return {
            "user_id": instance.user.id,
            "phone": instance.user.phone,
            "full_name": instance.full_name,
            "profile_id": instance.id,
            "detail": "Abituriyent va profil yaratildi."
        }
