from django.db import models


class ApplicationNotification(models.Model):
    application = models.ForeignKey(
        "jobs.Application",
        on_delete=models.CASCADE,
        related_name="application_notifications",
    )
    sender = models.ForeignKey(
        "jobseeker.JobseekerProfile",
        on_delete=models.CASCADE,
        related_name="application_notifications",
    )
    receiver = models.ForeignKey(
        "employer.Employer",
        on_delete=models.CASCADE,
        related_name="application_notifications",
    )
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # order by is_read and timestamp,
        # unread notifications at the top and
        # the oldest notifications at the bottom
        ordering = ["-is_read", "-timestamp"]
        verbose_name_plural = "application_notifications"
