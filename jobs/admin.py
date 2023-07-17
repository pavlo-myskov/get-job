from django.contrib import admin

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

from .models import Vacancy, Application


def send_vacancy_approved_email(obj):
    """Send email to the employer when the job post is approved"""

    # Check if the employer has enabled email notifications
    if not obj.employer.email_notifications:
        return

    current_site = get_current_site(None)

    subject = "Vacancy Approved!"
    message = (
        f"Hello {obj.employer.employerprofile.name},\n\n"
        f"Your job post {obj.title} has been approved!\n"
        "Please check your dashboard for more details.\n\n"
        f"Thank you for using {current_site.name} service!\n"
        f"{current_site.domain}"
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[obj.employer.email],
        fail_silently=True,
    )


def send_vacancy_rejected_email(obj):
    """Send email to the employer when the job post is rejected"""

    # Check if the employer has enabled email notifications
    if not obj.employer.email_notifications:
        return

    current_site = get_current_site(None)

    subject = "Vacancy Rejected!"
    message = (
        f"Hello {obj.employer.employerprofile.name},\n\n"
        f"Your job post {obj.title} has been rejected!\n"
        "It does not meet our requirements. Please, "
        "make sure that the job post is complete.\n\n"
        "Check your dashboard for more details.\n"
        f"Thank you for using {current_site.name} service!\n\n"
        f"{current_site.domain}"
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[obj.employer.email],
        fail_silently=True,
    )


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    """Define admin model for custom Vacancy model."""

    # The fields which displayed in the list of vacancies in admin panel
    list_display = (
        "title",
        "status",
        "employer",
        "area",
        "job_location",
        "job_type",
        "salary",
        "experience_duration",
        "updated_on",
        "created_on",
    )
    # list of fields to generate filters in the right sidebar of admin panel
    list_filter = (
        "status",
        "job_type",
        "job_location",
        "area",
    )
    search_fields = ("title", "body")

    # Sorted by vacancies that are in review and with the oldest created date
    ordering = ("-status", "updated_on")

    actions = ["approve_job_posts", "reject_job_posts", "close_job_posts"]

    def approve_job_posts(self, request, queryset):
        queryset.update(status=Vacancy.JobPostStatus.ACTIVE)
        for job in queryset:
            send_vacancy_approved_email(job)

    def reject_job_posts(self, request, queryset):
        queryset.update(status=Vacancy.JobPostStatus.REJECTED)
        for job in queryset:
            send_vacancy_rejected_email(job)

    def close_job_posts(self, request, queryset):
        queryset.update(status=Vacancy.JobPostStatus.CLOSED)

    def save_model(self, request, obj, form, change):
        """
        Send email to the employer when the job post is approved or rejected
        """

        # Check if Vacancy object is changed, but not created
        if change:
            old_obj = Vacancy.objects.get(pk=obj.pk)

            # Compare the status of the old object with the new one
            if old_obj.status != obj.status:

                # send email to the employer with the status of the job post
                if obj.status == Vacancy.JobPostStatus.ACTIVE:
                    send_vacancy_approved_email(obj)

                # send email to the employer with the status of the job post
                elif obj.status == Vacancy.JobPostStatus.REJECTED:
                    send_vacancy_rejected_email(obj)

        return super().save_model(request, obj, form, change)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Define admin model for custom Application model."""

    # The fields which displayed in the list of applications in admin panel
    list_display = (
        "vacancy",
        "applicant",
        "resume",
        "applied_on",
    )
    # list of fields to generate filters in the right sidebar of admin panel
    list_filter = (
        "vacancy",
        "applicant",
    )
    search_fields = ("vacancy", "applicant")
