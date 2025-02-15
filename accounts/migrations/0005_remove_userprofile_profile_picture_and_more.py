# Generated by Django 5.0 on 2024-01-30 07:16

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_user_profile_picture_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.models.UserImagePath('profile_pictures')),
        ),
    ]
