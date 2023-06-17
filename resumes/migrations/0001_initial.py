# Generated by Django 3.2.19 on 2023-06-17 10:16

import cloudinary_storage.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobseeker', '0002_jobseekerprofile_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupation', models.CharField(max_length=254)),
                ('experience', models.TextField()),
                ('education', models.TextField()),
                ('skills', models.TextField()),
                ('body', models.TextField()),
                ('cv', models.FileField(blank=True, storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(), upload_to='cv/')),
                ('jobseeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to='jobseeker.jobseeker')),
            ],
        ),
    ]