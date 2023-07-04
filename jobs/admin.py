from django.contrib import admin

from .models import Vacancy, Application


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    '''Define admin model for custom Vacancy model.'''

    # The fields which displayed in the list of vacancies in admin panel
    list_display = (
        "title",
        "status",
        # "employer",
        # "company",
        "area",
        "job_location",
        "job_type",
        "salary",
        "experience",
        "created_on",
    )
    # list of fields to generate filters in the right sidebar of admin panel
    list_filter = (
        "status",
        # "employer",
        # "company",
        "job_type",
        "job_location",
        "area",
    )
    search_fields = ("title", "body")

    # Sorted by vacancies that are in review and with the oldest created date
    ordering = ("status", "created_on")

    actions = ['approve_job_posts', 'reject_job_posts', 'close_job_posts']

    def approve_job_posts(self, request, queryset):
        queryset.update(status=Vacancy.JobPostStatus.ACTIVE)

    def reject_job_posts(self, request, queryset):
        queryset.update(status=Vacancy.JobPostStatus.REJECTED)

    def close_job_posts(self, request, queryset):
        queryset.update(status=Vacancy.JobPostStatus.CLOSED)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    '''Define admin model for custom Application model.'''

    # The fields which displayed in the list of applications in admin panel
    list_display = (
        "vacancy",
        "applicant",
        "applyed_on",
    )
    # list of fields to generate filters in the right sidebar of admin panel
    list_filter = (
        "vacancy",
        "applicant",
    )
    search_fields = ("vacancy", "applicant")
