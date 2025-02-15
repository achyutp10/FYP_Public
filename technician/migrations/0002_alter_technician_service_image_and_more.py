# Generated by Django 5.0 on 2024-01-30 06:07

import technician.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technician', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technician',
            name='service_image',
            field=models.ImageField(blank=True, null=True, upload_to=technician.models.TechnicianImagePath('serviceImages')),
        ),
        migrations.AlterField(
            model_name='technician',
            name='service_type',
            field=models.CharField(choices=[('PLUMBER', 'Plumber'), ('ELECTRICIAN', 'Electrician'), ('PANITER', 'Painter'), ('CARPENTER', 'Carpenter'), ('PEST', 'Pest')], default='PLUMBER', max_length=25),
        ),
        migrations.AlterField(
            model_name='technician',
            name='technician_license',
            field=models.ImageField(blank=True, null=True, upload_to=technician.models.TechnicianImagePath('license')),
        ),
    ]
