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

    def reject_resumes(self, request, queryset):
        queryset.update(status=Resume.ResumePublishStatus.REJECTED)

    def close_resumes(self, request, queryset):
        queryset.update(status=Resume.ResumePublishStatus.CLOSED)
