# Generated by Django 5.2 on 2025-05-08 11:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('diploms', '0001_initial'),
        ('programs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admission_type', models.CharField(choices=[('regular', '1st Year (New Admission)'), ('transfer', 'Transfer (Perevod)')], default='regular', max_length=20)),
                ('contract_file', models.FileField(blank=True, null=True, upload_to='contracts/')),
                ('status', models.CharField(choices=[('pending', 'Submitted'), ('review', 'Under Review'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.branch')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='diploms.course')),
                ('diplom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='diploms.diplom')),
                ('education_form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.educationform')),
                ('education_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.educationlevel')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.program')),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_applications', to=settings.AUTH_USER_MODEL)),
                ('transfer_diplom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='diploms.transferdiplom')),
                ('user', models.ForeignKey(limit_choices_to={'role': 'APPLICANT'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
