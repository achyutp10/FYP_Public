# Generated by Django 5.0 on 2024-01-30 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('technician', '0003_technician_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='technician',
            name='profile_picture',
        ),
    ]
