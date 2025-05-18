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

# --- Telefon formatini +998 bilan normalize qilish ---
def normalize_phone(phone):
    if not phone.startswith('+998'):
        raise serializers.ValidationError("Telefon raqam faqat +998 bilan boshlanishi kerak.")
    return phone


# --- Combined login/register with optional telegram_id ---
class CombinedAuthSerializer(serializers.Serializer):
    phone = serializers.CharField()
    telegram_id = serializers.CharField(required=False, allow_blank=True, write_only=True)

    def validate_phone(self, value):
        return normalize_phone(value)

    def create(self, validated_data):
        phone = validated_data['phone']
        telegram_id = validated_data.get('telegram_id')

        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={'is_verified': False}
        )

        # 🟡 Agar telegram_id mavjud bo‘lsa, yangilaymiz
        if telegram_id and (not user.telegram_id or user.telegram_id != telegram_id):
            user.telegram_id = telegram_id
            user.save(update_fields=['telegram_id'])

        # if not can_send_code(phone):
        #     raise serializers.ValidationError("Tasdiqlash kodi allaqachon yuborilgan. 1 daqiqa kuting.")

        code = generate_code()
        PhoneVerification.objects.create(phone=phone, code=code)
        send_sms(phone, f"Xalqaro innovatsion universiteti qabul tizimiga kirish kodingiz: {code}")

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
        phone = normalize_phone(attrs['phone'])
        code = attrs['code']
        try:
            verification = PhoneVerification.objects.filter(phone=phone, code=code).latest('created_at')
        except PhoneVerification.DoesNotExist:
            raise serializers.ValidationError("Tasdiqlash kodi noto‘g‘ri.")
        if verification.is_expired():
            raise serializers.ValidationError("Kod eskirgan.")
        attrs['phone'] = phone
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
        phone = normalize_phone(value)
        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("Bunday foydalanuvchi topilmadi.")
        return phone

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
        phone = normalize_phone(attrs['phone'])
        code = attrs['code']
        try:
            verification = PhoneVerification.objects.filter(phone=phone, code=code).latest('created_at')
        except PhoneVerification.DoesNotExist:
            raise serializers.ValidationError("Kod noto‘g‘ri.")
        if verification.is_expired():
            raise serializers.ValidationError("Kod eskirgan.")
        attrs['phone'] = phone
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
            'id', 'last_name', 'first_name', 'other_name',
            'birth_date', 'passport_series', 'pinfl',
            'country', 'region', 'district', 'address',
            'gender', 'nationality', 'image', 'passport_file'
        ]

    def validate(self, attrs):
        # Validatsiyadan o‘tkazamiz, lekin xatolik qaytarmaymiz
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user

        # Agar profil allaqachon mavjud bo‘lsa, uni qaytaramiz
        if hasattr(user, 'applicant_profile'):
            return user.applicant_profile

        # Yangi profil yaratamiz
        profile = ApplicantProfile.objects.create(user=user, **validated_data)
        return profile


# --- Komissiya tomonidan Applicant yaratish ---
class ApplicantCreateByStaffSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    other_name = serializers.CharField(required=False)

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
            'phone', 'last_name', 'first_name', 'other_name',
            'birth_date', 'passport_series', 'pinfl',
            'country', 'region', 'district', 'address',
            'gender', 'nationality', 'image', 'passport_file'
        ]

    def validate_phone(self, value):
        phone = normalize_phone(value)
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("Bu telefon raqam bilan foydalanuvchi allaqachon mavjud.")
        return phone

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        last_name = validated_data.pop('last_name')
        first_name = validated_data.pop('first_name')
        other_name = validated_data.pop('other_name', '')

        user = User.objects.create(
            phone=phone,
            last_name=last_name,
            first_name=first_name,
            other_name=other_name,
            role='APPLICANT',
            is_verified=True
        )
        profile = ApplicantProfile.objects.create(user=user, **validated_data)
        return profile
