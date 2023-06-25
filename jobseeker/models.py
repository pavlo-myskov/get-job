from cloudinary.models import CloudinaryField

from django.urls import reverse
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model

from jobs.models import Vacancy

User = get_user_model()


class JobseekerManager(BaseUserManager):
    """
    Custom manager that allows to use this proxy model
    to work with Jobseeker data only
    Examples:
    """

    def get_queryset(self, *args, **kwargs):
        """Return only Jobseeker users"""
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.JOBSEEKER)


class Jobseeker(User):
    """
    Interface to access User model with Jobseeker role
    without creating a new table in Database

    Examples:
    >>> from .models import Jobseeker

    - Create a new Jobseeker user (automatically assign role=JOBSEEKER):

    >>> Jobseeker.objects.create_user(username="jobseeker1", password="123456")

    - Get all Jobseekers:

    >>> Jobseeker.jobseeker.all()

    - Get a specific Jobseeker:

    >>> Jobseeker.jobseeker.get(username="jobseeker1")
    """

    # override the default base_role
    base_role = User.Role.JOBSEEKER
    jobseeker = JobseekerManager()

    class Meta:
        proxy = True

    @property
    def profile(self):
        """
        Returns JobseekerProfile object.
        It allows to access JobseekerProfile data for a specific Jobseeker.
        """
        return self.jobseekerprofile

    def welcome_message(self):
        """Example of a custom method for Jobseeker model"""
        return "Only Jobseeker can see this message"

    # override save method
    def save(self, *args, **kwargs):
        """If user is not created yet,
        Create a new user with base role"""
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)


class JobseekerProfile(models.Model):
    """Table to store Jobseeker profile data.

    Access JobseekerProfile data for a specific Jobseeker using
    Jobseeker.profile property:
     >>> j1 = Jobseeker.jobseeker.get(username="jobseeker1")
    >>> j1.profile
    <JobseekerProfile: JobseekerProfile object (1)>

    To populate JobseekerProfile data:
    >>> j1.profile.address = "123 Main St"
    >>> j1.profile.save()

    To get Jobseeker users with specific JobseekerProfile data:
    >>> Jobseeker.objects.filter(jobseekerprofile__age="30")
    """

    GENDER_TYPES = (
        ("F", "Female"),
        ("M", "Male"),
        ("O", "Other"),
    )

    user = models.OneToOneField(Jobseeker, on_delete=models.CASCADE)
    # use name instead of first_name and last_name,
    # as they don't cover global name patterns
    name = models.CharField(max_length=254)
    avatar = CloudinaryField("avatar", blank=True, null=True)
    gender = models.CharField(
        choices=GENDER_TYPES, max_length=10, blank=True, null=True
    )
    dob = models.DateField(blank=True, null=True)
    address = models.TextField(max_length=1000, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    applications = models.ManyToManyField(
        Vacancy, blank=True, related_name="applicants"
    )
    favorites = models.ManyToManyField(
        Vacancy, blank=True, related_name="favoriters"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # if avatar is not set, use the default avatar
        if not self.avatar:
            self.avatar = "media/get-job/profile_placehoder.png"
            self.save()

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("jobseeker_home")
        # TODO: create a profile page for Jobseeker
        # return reverse("jobseeker_profile")


@receiver(post_save, sender=Jobseeker)
def create_jobseeker_profile(sender, instance, created, **kwargs):
    """
    Using signals, Create a JobseekerProfile
    when a new Jobseeker user is created
    """
    if created and instance.role == "JOBSEEKER":
        JobseekerProfile.objects.create(user=instance)
