# Generated by Django 5.0 on 2024-02-29 09:42

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('technician', '0005_technician_is_available_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(blank=True, max_length=250, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True)),
                ('booking_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('ACCEPT', 'Accept'), ('REJECT', 'Reject'), ('COMPLETED', 'Completed'), ('PENDING', 'Pending')], default='PENDING', max_length=100)),
                ('is_paid', models.BooleanField(default=False)),
                ('technician', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='technician.technician')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
