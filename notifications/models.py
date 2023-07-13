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


class JobOfferNotification(models.Model):
    job_offer = models.ForeignKey(
        "employer.JobOffer",
        on_delete=models.CASCADE,
        related_name="job_offer_notifications",
    )
    sender = models.ForeignKey(
        "employer.Employer",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        "jobseeker.Jobseeker",
        on_delete=models.CASCADE,
        related_name="job_offer_notifications",
    )
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # order by is_read and timestamp,
        # unread notifications at the top and
        # the oldest notifications at the bottom
        ordering = ["-is_read", "-timestamp"]
        verbose_name_plural = "job offer notifications"
