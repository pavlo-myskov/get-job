# Generated by Django 3.2.19 on 2023-06-29 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0007_resume_updated_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='status',
            field=models.CharField(choices=[('IN_REVIEW', 'In Review'), ('ACTIVE', 'Active'), ('REJECTED', 'Rejected'), ('CLOSED', 'Closed')], default='IN_REVIEW', max_length=50),
        ),
    ]
