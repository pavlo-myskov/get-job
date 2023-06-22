# Generated by Django 3.2.19 on 2023-06-22 11:05

from django.db import migrations
import jobseeker.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseeker', '0006_alter_jobseekerprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='avatar',
            field=jobseeker.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='avatar'),
        ),
    ]