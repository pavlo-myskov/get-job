from django.contrib import admin

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

from .models import Resume


def send_resume_approved_email(obj):
    """Send email to the jobseeker when the resume is approved"""

    # Check if the jobseeker has enabled email notifications
    if not obj.jobseeker.email_notifications:
        return

    current_site = get_current_site(None)

    subject = "Resume Approved!"
    message = (
        f"Hello {obj.jobseeker.jobseekerprofile.name},\n\n"
        f"Your resume {obj.occupation} has been approved!\n"
        "Please check your dashboard for more details.\n\n"
        f"Thank you for using {current_site.name} service!\n"
        f"{current_site.domain}"
    )
    # send email to the jobseeker with the status of the resume
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[obj.jobseeker.email],
        fail_silently=True,
    )


def send_resume_rejected_email(obj):
    """Send email to the jobseeker when the resume is rejected"""

    # Check if the jobseeker has enabled email notifications
    if not obj.jobseeker.email_notifications:
        return

    current_site = get_current_site(None)

    subject = "Resume Rejected!"
    message = (
        f"Hello {obj.jobseeker.jobseekerprofile.name},\n\n"
        f"Your resume {obj.occupation} has been rejected!\n"
        "It does not meet our requirements. Please, "
        "make sure that the resume is complete.\n\n"
        "Check your dashboard for more details.\n"
        f"Thank you for using {current_site.name} service!\n\n"
        f"{current_site.domain}"
    )
    # send email to the jobseeker with the status of the resume
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[obj.jobseeker.email],
        fail_silently=True,
    )


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """Define admin model for Resume model."""

    list_display = [
        "jobseeker",
        "status",
        "occupation",
        "experience_duration",
        "updated_on",
        "created_on",
    ]
    list_filter = ("status", "experience_duration",)
    search_fields = ["jobseeker__email", "occupation", "skills"]
    # Sorted by resumes that are in review and with the oldest updated_on date
    ordering = ("-status", "updated_on")

    actions = ["approve_resumes", "reject_resumes", "close_resumes"]

    def approve_resumes(self, request, queryset):
        queryset.update(status=Resume.ResumePublishStatus.ACTIVE)
        for resume in queryset:
            send_resume_approved_email(resume)

    def reject_resumes(self, request, queryset):
        queryset.update(status=Resume.ResumePublishStatus.REJECTED)
        for resume in queryset:
            send_resume_rejected_email(resume)

    def close_resumes(self, request, queryset):
        queryset.update(status=Resume.ResumePublishStatus.CLOSED)

    def save_model(self, request, obj, form, change):
        """
        Send email to the jobseeker when the resume is approved or rejected
        """

        # Check if Resume object is changed, but not created
        if change:
            old_obj = Resume.objects.get(pk=obj.pk)

            # Compare the status of the old object with the new one
            if old_obj.status != obj.status:
                # send email to the jobseeker with the status of the resume
                if obj.status == Resume.ResumePublishStatus.ACTIVE:
                    send_resume_approved_email(obj)

                # send email to the jobseeker with the status of the resume
                elif obj.status == Resume.ResumePublishStatus.REJECTED:
                    send_resume_rejected_email(obj)

        return super().save_model(request, obj, form, change)
