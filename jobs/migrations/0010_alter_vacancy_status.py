# Generated by Django 3.2.19 on 2023-06-29 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_alter_vacancy_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='status',
            field=models.CharField(choices=[('IN_REVIEW', 'In Review'), ('ACTIVE', 'Active'), ('REJECTED', 'Rejected'), ('CLOSED', 'Closed')], default='IN_REVIEW', max_length=50),
        ),
    ]