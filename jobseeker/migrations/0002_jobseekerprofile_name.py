# Generated by Django 3.2.19 on 2023-06-17 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseeker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseekerprofile',
            name='name',
            field=models.CharField(blank=True, max_length=254),
        ),
    ]
