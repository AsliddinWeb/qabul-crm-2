from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Foydalanuvchi uchun telefon raqam kiritilishi shart.")
        phone = self.normalize_email(phone)  # Telefon uchun normalize shart emas, lekin saqladik
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_applicant(self, phone, full_name=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'APPLICANT')
        user = self.create_user(phone, password, full_name=full_name, **extra_fields)
        return user

    def create_staff(self, phone, full_name=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'STAFF')
        extra_fields.setdefault('is_staff', True)
        user = self.create_user(phone, password, full_name=full_name, **extra_fields)
        return user

    def create_admin(self, phone, full_name=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'ADMIN')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if password is None:
            raise ValueError("Admin uchun parol majburiy.")
        return self.create_user(phone, password, full_name=full_name, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        # Django standart superuser uchun
        extra_fields.setdefault('role', 'ADMIN')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if password is None:
            raise ValueError("Superuser uchun parol majburiy.")
        return self.create_user(phone, password, **extra_fields)
