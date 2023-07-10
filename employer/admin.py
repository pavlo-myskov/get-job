from django.contrib import admin

from .models import EmployerProfile, JobOffer


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    '''Define admin model for EmployerProfile model.'''

    list_display = ['user', 'name', 'company']
    search_fields = ['user__email', 'name', 'company']


@admin.register(JobOffer)
class ApplicationAdmin(admin.ModelAdmin):
    '''Define admin model for JobOffer model.'''

    list_display = (
        "resume",
        "employer",
        "vacancy",
        "offered_on"
    )
    list_filter = (
        "resume",
        "employer",
    )
    search_fields = ("resume", "employer", "vacancy",)
