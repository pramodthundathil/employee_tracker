# Generated by Django 5.0.6 on 2025-01-23 15:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_customuser_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_marked', models.BooleanField(default=False)),
                ('attendance', models.CharField(blank=True, choices=[('Present', 'Present'), ('Absent', 'Absent')], max_length=20, null=True)),
                ('attendance_status', models.BooleanField(blank=True, null=True)),
                ('in_date_time', models.DateTimeField(auto_now_add=True)),
                ('out_date_time', models.DateTimeField(auto_now_add=True)),
                ('approve', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
