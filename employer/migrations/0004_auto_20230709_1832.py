# Generated by Django 3.2.19 on 2023-07-09 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0003_joboffer'),
    ]

    operations = [
        migrations.AddField(
            model_name='joboffer',
            name='resume_snapshot',
            field=models.JSONField(),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='vacancy_snapshot',
            field=models.JSONField(),
        ),
    ]
