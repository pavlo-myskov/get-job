# Generated by Django 3.2.19 on 2023-06-02 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('area', models.CharField(choices=[('DUBLIN', 'Dublin'), ('DUBLIN_CITY_CENTRE', 'Dublin City Centre'), ('DUBLIN_NORTH', 'Dublin North'), ('DUBLIN_SOUTH', 'Dublin South'), ('DUBLIN_WEST', 'Dublin West'), ('CARLOW', 'Carlow'), ('CAVAN', 'Cavan'), ('CLARE', 'Clare'), ('CORK', 'Cork'), ('DONEGAL', 'Donegal'), ('GALWAY', 'Galway'), ('KERRY', 'Kerry'), ('KILDARE', 'Kildare'), ('KILKENNY', 'Kilkenny'), ('LAOIS', 'Laois'), ('LEITRIM', 'Leitrim'), ('LIMERICK', 'Limerick'), ('LONGFORD', 'Longford'), ('LOUTH', 'Louth'), ('MAYO', 'Mayo'), ('MEATH', 'Meath'), ('MONAGHAN', 'Monaghan'), ('OFFALY', 'Offaly'), ('ROSCOMMON', 'Roscommon'), ('SLIGO', 'Sligo'), ('TIPPERARY', 'Tipperary'), ('WATERFORD', 'Waterford'), ('WESTMEATH', 'Westmeath'), ('WEXFORD', 'Wexford'), ('WICKLOW', 'Wicklow'), ('NORTHERN_IRELAND', 'Northern Ireland'), ('UK', 'UK'), ('EUROPE', 'Europe'), ('WORLDWIDE', 'Worldwide')], max_length=50)),
                ('job_location', models.CharField(choices=[('ON_SITE', 'On Site'), ('REMOTE', 'Remote'), ('HYBRID', 'Hybrid')], max_length=50)),
                ('job_type', models.CharField(choices=[('FULL_TIME', 'Full Time'), ('PART_TIME', 'Part Time'), ('CONTRACT', 'Contract'), ('PERMANENT', 'Permanent'), ('TEMPORARY', 'Temporary'), ('INTERNSHIP', 'Internship'), ('VOLUNTEER', 'Volunteer')], max_length=50)),
                ('salary', models.CharField(default='Negotiable', max_length=50)),
                ('experience', models.CharField(blank=True, max_length=50, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'IN_REVIEW'), (1, 'ACTIVE'), (2, 'CLOSED')], default=0)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
