from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from employer.views import EmployerRequiredMixin
from jobportal.base_views import JobSearchFormMixin, ResumeSearchFormMixin
from jobseeker.views import JobseekerRequiredMixin
from notifications.models import ApplicationNotification, JobOfferNotification


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

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        notification = get_object_or_404(ApplicationNotification, pk=pk)
        notification.is_read = True
        notification.save()

        # get the number of unread notifications using
        # the custom method on the User model
        counter = request.user.unread_application_notifications_count()
        return JsonResponse({"counter": counter})


class ApplicationNotificationReadAll(EmployerRequiredMixin, View):
    """Set all application notifications as read and update page"""

    def post(self, request, *args, **kwargs):
        notifications = request.user.unread_application_notifications()
        notifications.update(is_read=True)
        messages.success(request, "All notifications marked as read")
        return HttpResponseRedirect(reverse("application_notifications"))


class JobOfferNotificationList(
    JobseekerRequiredMixin, JobSearchFormMixin, ListView
):
    template_name = 'notifications/job_offer_notifications.html'
    context_object_name = "notifications"

    def get_queryset(self):
        """Return the notifications for the current user"""
        return self.request.user.job_offer_notifications.all()

    def get(self, request, *args, **kwargs):
        """Add message if there are no notifications"""
        response = super().get(request, *args, **kwargs)
        if not self.object_list.filter(is_read=False).exists():
            messages.info(request, "There are currently no new applications")
        return response


class JobOfferNotificationToggleRead(JobseekerRequiredMixin, View):
    """Set the read status of an job offer notification"""

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        notification = get_object_or_404(JobOfferNotification, pk=pk)
        notification.is_read = True
        notification.save()

        # get the number of unread notifications using
        # the custom method on the User model
        counter = request.user.unread_job_offer_notifications_count()
        return JsonResponse({"counter": counter})


class JobOfferNotificationReadAll(JobseekerRequiredMixin, View):
    """Set all job offer notifications as read and update page"""

    def post(self, request, *args, **kwargs):
        notifications = request.user.unread_job_offer_notifications()
        notifications.update(is_read=True)
        messages.success(request, "All notifications marked as read")
        return HttpResponseRedirect(reverse("job_offer_notifications"))
