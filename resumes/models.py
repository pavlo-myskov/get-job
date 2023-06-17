from django.db import models

from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import RawMediaCloudinaryStorage

from jobseeker.models import Jobseeker


class Resume(models.Model):
    class ResumePublishStatus(models.TextChoices):
        IN_REVIEW = "IN_REVIEW", "In Review"
        ACTIVE = "ACTIVE", "Active"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"
        CLOSED = "CLOSED", "Closed"

    class Duration(models.TextChoices):
        LESS_THAN_1_YEAR = "LESS_THAN_1_YEAR", "Less than 1 year"
        ONE_TO_2_YEARS = "ONE_TO_2_YEARS", "1 to 2 years"
        TWO_TO_5_YEARS = "TWO_TO_5_YEARS", "2 to 5 years"
        FIVE_TO_10_YEARS = "FIVE_TO_10_YEARS", "5 to 10 years"
        MORE_THAN_10_YEARS = "MORE_THAN_10_YEARS", "More than 10 years"

    jobseeker = models.ForeignKey(
        Jobseeker, on_delete=models.CASCADE, related_name="resumes"
    )
    occupation = models.CharField(max_length=254)
    experience_duration = models.CharField(
        choices=Duration.choices, max_length=50, null=True
    )
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    body = models.TextField(blank=True)
    cv = models.FileField(
        upload_to="cv/", blank=True, storage=RawMediaCloudinaryStorage()
    )
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=ResumePublishStatus.choices,
        max_length=50,
        default=ResumePublishStatus.IN_REVIEW,
    )

    class Meta:
        # ordered by the date they were created,
        # with the most recent ones at the top
        ordering = ["-created_on"]

    def __str__(self) -> str:
        return f"{self.occupation} - {self.jobseeker}"

    # TODO:
    # def get_absolute_url(self):
    #     return reverse("resumes:resume_detail", args=[str(self.id)])
