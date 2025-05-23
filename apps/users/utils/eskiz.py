from eskiz.client.sync import ClientSync
from django.conf import settings


def get_eskiz_client():
    client = ClientSync(email=settings.ESKIZ_EMAIL, password=settings.ESKIZ_PASSWORD)
    try:
        client.login()
    except Exception as e:
        print(f"Eskiz login failed: {e}")
        raise
    return client


def normalize_phone(phone):
    """
    Telefon raqamni 998 bilan boshlanuvchi formatga keltiradi.
    Masalan: +998901234567 -> 998901234567
    """
    if phone.startswith('+'):
        phone = phone[1:]
    return phone


def send_sms(phone, message):
    """
    Telefon raqamga SMS yuboradi. phone: `998901234567` formatida bo'lishi kerak.
    """
    phone = normalize_phone(phone)
    try:
        client = get_eskiz_client()
        response = client.send_sms(phone_number=phone, message=message)
        return response
    except Exception as e:
        print(f"Eskiz SMS yuborishda xatolik: {e}")
        return None
