from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView

from employer.views import EmployerRequiredMixin
from jobportal.base_views import ResumeSearchFormMixin
from notifications.models import ApplicationNotification


class ApplicationNotificationList(
    EmployerRequiredMixin, ResumeSearchFormMixin, ListView
):
    template_name = 'notifications/application_notifications.html'
    context_object_name = "notifications"

    def get_queryset(self):
        """Return the notifications for the current user"""
        return self.request.user.application_notifications.all()
