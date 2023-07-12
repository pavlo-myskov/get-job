# Generated by Django 3.2.19 on 2023-07-12 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0009_alter_resume_cv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='resume',
            name='experience_duration',
            field=models.CharField(choices=[('LESS_THAN_1_YEAR', 'Less than 1 year'), ('ONE_TO_2_YEARS', '1 to 2 years'), ('TWO_TO_5_YEARS', '2 to 5 years'), ('FIVE_TO_10_YEARS', '5 to 10 years'), ('MORE_THAN_10_YEARS', 'More than 10 years')], max_length=50),
        ),
        migrations.AlterField(
            model_name='resume',
            name='skills',
            field=models.TextField(),
        ),
    ]