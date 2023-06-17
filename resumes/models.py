from django.db import models

from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import RawMediaCloudinaryStorage

from jobseeker.models import Jobseeker


class Resume(models.Model):
    jobseeker = models.ForeignKey(
        Jobseeker, on_delete=models.CASCADE, related_name="resumes"
    )
    occupation = models.CharField(max_length=254)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    body = models.TextField(blank=True)
    cv = models.FileField(
        upload_to="cv/", blank=True, storage=RawMediaCloudinaryStorage()
    )

    def __str__(self) -> str:
        return f'{self.occupation} - {self.jobseeker}'
