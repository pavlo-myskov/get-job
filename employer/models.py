from cloudinary.models import CloudinaryField

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model

User = get_user_model()


class EmployerManager(BaseUserManager):
    """
    Custom manager that allows to use this proxy model
    to work with Employer data only
    Examples:
    >>> from .models import Employer
    >>> Employer.objects.all()
    <QuerySet [<Employer: employer1>, <Employer: employer2>]>
    """

    def get_queryset(self, *args, **kwargs):
        """Return only Employer users"""
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.EMPLOYER)


class Employer(User):
    """
    Interface to access User model with Employer role
    without creating a new table in Database

    Examples:
    >>> from .models import Employer

    - Create a new Employer user (automatically assign role=EMPLOYER):

    >>> Employer.objects.create_user(
        email="employer1@email.com", password="123456"
        )

    - Get all Employers:

    >>> Employer.employer.all()

    - Get a specific Employer:

    >>> Employer.employer.get(email="employer1@email.com")
    """

    # override the default base_role
    base_role = User.Role.EMPLOYER
    employer = EmployerManager()

    class Meta:
        proxy = True

    @property
    def profile(self):
        """
        Returns EmployerProfile object.
        It allows to access EmployerProfile data for a specific Employer.
        """
        return self.employerprofile

    def welcome_message(self):
        """Example of a custom method for Employer model"""
        return "Only Employer can see this message"

    # override save method
    def save(self, *args, **kwargs):
        """If user is not created yet,
        Create a new user with base role"""
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)


class EmployerProfile(models.Model):
    """Table to store Employer profile data.

    Access EmployerProfile data for a specific Employer using
    Employer.profile property:
    >>> emp1 = Employer.employer.get(email="employer1@email.com")
    >>> emp1.profile
    <EmployerProfile: EmployerProfile object (1)>

    To populate EmployerProfile data:
    >>> emp1.profile.company = "Company 1"
    >>> emp1.profile.save()

    To get Employer users with specific EmployerProfile data:
    >>> Employer.objects.filter(employerprofile__company="company 1")
    """

    user = models.OneToOneField(Employer, on_delete=models.CASCADE)
    # use name instead of first_name and last_name,
    # as they don't cover global name patterns
    name = models.CharField(max_length=254, blank=True)
    company = models.CharField(max_length=254, blank=True)
    logo = CloudinaryField("logo", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(max_length=254, blank=True)
    favorites = models.ManyToManyField(
        'resumes.Resume', blank=True, related_name="favoriters"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # if avatar is not set, use the default avatar
        if not self.logo:
            self.logo = "media/get-job/company_placeholder"
            self.save()

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return f"/employer/profile/{self.pk}/"


@receiver(post_save, sender=Employer)
def create_employer_profile(sender, instance, created, **kwargs):
    """
    Using signals, Create a EmployerProfile
    when a new Employer user is created
    """
    if created and instance.role == "EMPLOYER":
        EmployerProfile.objects.create(user=instance)
