# Generated by Django 3.2.19 on 2023-06-02 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancy',
            options={'ordering': ['-created_on'], 'verbose_name_plural': 'vacancies'},
        ),
    ]