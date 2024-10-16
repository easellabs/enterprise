# Generated by Django 5.1.1 on 2024-10-07 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
        ("otp_totp", "0003_add_timestamps"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomTOTPDevice",
            fields=[
                (
                    "totpdevice_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="otp_totp.totpdevice",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("otp_totp.totpdevice",),
        ),
        migrations.AlterModelOptions(
            name="customuser",
            options={},
        ),
        migrations.AlterModelManagers(
            name="customuser",
            managers=[],
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="date_joined",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="is_verified",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="phone_number",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="role",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="username",
        ),
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="first_name",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="is_staff",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="last_name",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
