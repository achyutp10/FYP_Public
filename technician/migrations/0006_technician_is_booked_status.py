# Generated by Django 5.0 on 2024-04-07 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technician', '0005_technician_is_available_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='technician',
            name='is_booked_status',
            field=models.BooleanField(default=False),
        ),
    ]
