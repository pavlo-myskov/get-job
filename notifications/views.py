from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
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

    def get(self, request, *args, **kwargs):
        """Add message if there are no notifications"""
        response = super().get(request, *args, **kwargs)
        if not self.object_list.filter(is_read=False).exists():
            messages.info(request, "There are currently no new applications")
        return response


class ApplicationNotificationToggleRead(EmployerRequiredMixin, View):
    """Set the read status of an application notification"""

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        notification = get_object_or_404(ApplicationNotification, pk=pk)
        notification.is_read = True
        notification.save()

        # get the number of unread notifications using
        # the custom method on the User model
        counter = request.user.unread_application_notifications_count()
        return JsonResponse({"counter": counter})
