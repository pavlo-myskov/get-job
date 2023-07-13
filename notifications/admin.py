from django.contrib import admin

from .models import ApplicationNotification, JobOfferNotification


@admin.register(ApplicationNotification)
class ApplicationNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "sender",
        "receiver",
        "is_read",
        "timestamp",
    )
    search_fields = ("sender", "receiver")


@admin.register(JobOfferNotification)
class JobOfferNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "job_offer",
        "sender",
        "receiver",
        "is_read",
        "timestamp",
    )
    search_fields = ("sender", "receiver")
