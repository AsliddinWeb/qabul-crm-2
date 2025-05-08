from django import forms
from .models import Application

class ApplicationAdminForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        user = cleaned_data.get('user')
        diplom = cleaned_data.get('diplom')
        transfer_diplom = cleaned_data.get('transfer_diplom')
        admission_type = cleaned_data.get('admission_type')
        program = cleaned_data.get('program')
        branch = cleaned_data.get('branch')
        education_level = cleaned_data.get('education_level')
        education_form = cleaned_data.get('education_form')

        # ✅ Telegram ID bo‘lsa diplom tekshiruvi o‘tkazilmaydi
        skip_diploma_check = bool(user and user.telegram_id)

        if not skip_diploma_check:
            if admission_type == 'transfer':
                if not transfer_diplom:
                    raise forms.ValidationError("Transfer qabuli uchun transfer diplom kerak.")
                if diplom:
                    raise forms.ValidationError("Transferda oddiy diplom bo‘lmasligi kerak.")
                if transfer_diplom.user != user:
                    raise forms.ValidationError("Transfer diplom foydalanuvchisi ariza egasi bilan mos emas.")
            else:
                if not diplom:
                    raise forms.ValidationError("Yangi qabul uchun diplom kerak.")
                if transfer_diplom:
                    raise forms.ValidationError("Yangi qabulda transfer diplom kerak emas.")
                if diplom.user != user:
                    raise forms.ValidationError("Diplom foydalanuvchisi ariza egasi bilan mos emas.")

        # ✅ Bu qism har doim ishlaydi — hatto telegram_id bo‘lsa ham
        if program:
            if program.branch != branch:
                raise forms.ValidationError({
                    'branch': f"Tanlangan yo'nalish faqat {program.branch.name} filialiga tegishli."
                })
            if program.education_level != education_level:
                raise forms.ValidationError({
                    'education_level': f"Tanlangan yo'nalish faqat {program.education_level.name} darajasida."
                })
            if program.education_form != education_form:
                raise forms.ValidationError({
                    'education_form': f"Tanlangan yo'nalish faqat {program.education_form.name} shaklida."
                })

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Course: faqat transfer diplom bo‘lsa
        if instance.transfer_diplom:
            instance.course = instance.transfer_diplom.target_course

        if commit:
            instance.save()
        return instance
