from django.contrib import admin

from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """Define admin model for Resume model."""

    list_display = [
        "jobseeker",
        "status",
        "occupation",
        "experience_duration",
        "created_on",
    ]
    list_filter = ("status", "experience_duration",)
    search_fields = ["jobseeker__email", "occupation", "skills"]
    # Sorted by resumes that are in review and with the oldest created date
    ordering = ("status", "created_on")

    actions = ["approve_resumes", "withdraw_resumes", "close_resumes"]

    def approve_resumes(self, request, queryset):
        queryset.update(status=Resume.ResumePublishStatus.ACTIVE)

    def withdraw_resumes(self, request, queryset):
        queryset.update(status=Resume.ResumePublishStatus.WITHDRAWN)

    def close_resumes(self, request, queryset):
        queryset.update(status=Resume.ResumePublishStatus.CLOSED)
