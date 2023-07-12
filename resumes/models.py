from cloudinary_storage.storage import RawMediaCloudinaryStorage

from django.db import models
from django.urls import reverse

from jobportal.validators import FileValidator, CV_TYPES

file_validator = FileValidator(
    max_size=512*1024,  # 500 KB
    content_types=CV_TYPES,
)


class ResumeManager(models.Manager):
    """Custom manager for the Resume model"""

    def active(self):
        """
        Return only active resumes.
        Example:
        >>> from resumes.models import Resume
        >>> Resume.objects.active()
        """
        return self.get_queryset().filter(
            status=Resume.ResumePublishStatus.ACTIVE
        )


class Resume(models.Model):
    class ResumePublishStatus(models.TextChoices):
        IN_REVIEW = "IN_REVIEW", "In Review"
        ACTIVE = "ACTIVE", "Active"
        REJECTED = "REJECTED", "Rejected"
        CLOSED = "CLOSED", "Closed"

    class Duration(models.TextChoices):
        LESS_THAN_1_YEAR = "LESS_THAN_1_YEAR", "Less than 1 year"
        ONE_TO_2_YEARS = "ONE_TO_2_YEARS", "1 to 2 years"
        TWO_TO_5_YEARS = "TWO_TO_5_YEARS", "2 to 5 years"
        FIVE_TO_10_YEARS = "FIVE_TO_10_YEARS", "5 to 10 years"
        MORE_THAN_10_YEARS = "MORE_THAN_10_YEARS", "More than 10 years"

    jobseeker = models.ForeignKey(
        "jobseeker.Jobseeker", on_delete=models.CASCADE, related_name="resumes"
    )
    occupation = models.CharField(max_length=254)
    experience_duration = models.CharField(
        choices=Duration.choices, max_length=50
    )
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    skills = models.TextField()
    body = models.TextField()
    cv = models.FileField(
        upload_to="get-job/cv/",
        blank=True,
        storage=RawMediaCloudinaryStorage(),
        validators=[file_validator],
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(
        choices=ResumePublishStatus.choices,
        max_length=50,
        default=ResumePublishStatus.IN_REVIEW,
    )

    objects = ResumeManager()

    class Meta:
        # ordered by the date they were created,
        # with the most recent ones at the top
        ordering = ["-created_on"]

    def __str__(self) -> str:
        return f"{self.occupation} - {self.jobseeker}"

    def get_absolute_url(self):
        return reverse("resume_detail", args=[str(self.pk)])
