from django.contrib import admin

from .models import ApplicationNotification


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
