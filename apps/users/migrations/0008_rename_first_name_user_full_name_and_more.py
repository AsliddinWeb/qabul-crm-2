# Generated by Django 5.2 on 2025-05-10 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_rename_full_name_user_first_name_user_last_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='full_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='other_name',
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='applicantprofile',
            name='other_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='applicantprofile',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
