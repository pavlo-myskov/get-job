from cloudinary.models import CloudinaryField
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator

from notifications.models import JobOfferNotification

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
    name = models.CharField(max_length=70)
    company = models.CharField(max_length=70, blank=True)
    logo = CloudinaryField("logo", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(max_length=254, blank=True)
    favorites = models.ManyToManyField(
        "resumes.Resume", blank=True, related_name="favoriters"
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


class JobOffer(models.Model):
    """Stores job offers"""

    resume = models.ForeignKey(
        "resumes.Resume", on_delete=models.CASCADE, related_name="job_offers"
    )
    resume_snapshot = models.JSONField()
    employer = models.ForeignKey(
        "employer.Employer",
        on_delete=models.CASCADE,
        related_name="job_offers",
    )
    vacancy = models.ForeignKey(
        "jobs.Vacancy", on_delete=models.CASCADE, related_name="job_offers"
    )
    vacancy_snapshot = models.JSONField()
    message = models.TextField(
        blank=True, validators=[MaxLengthValidator(1000)]
    )
    offered_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-offered_on"]

    def __str__(self):
        return f"{self.employer} - {self.resume}"


@receiver(post_save, sender=JobOffer)
def create_job_offer_notification(sender, instance, created, **kwargs):
    """Create a notification for the jobseeker
    when a new job offer is crefated"""
    if created:
        job_offer = instance

        JobOfferNotification.objects.create(
            job_offer=job_offer,
            sender=job_offer.employer,
            receiver=job_offer.resume.jobseeker,
        )

        # send email to jobseeker if email notification enabled
        if job_offer.vacancy.employer.email_notifications:
            current_site = get_current_site(None)
            job_offer_notifications_url = f"https://{current_site.domain}{reverse('job_offer_notifications')}"  # noqa
            message = render_to_string(
                "account/email/job_offer_notification.txt",
                {
                    "job_title": job_offer.vacancy.title,
                    "employer_name": job_offer.employer.employerprofile.name,
                    "employer_email": job_offer.employer.email,
                    "resume": job_offer.resume.occupation,
                    "site_url": job_offer_notifications_url,
                    "current_site": current_site,
                },
            )
        send_mail(
            subject="New job offer",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[job_offer.resume.jobseeker.email],
            fail_silently=False,
        )
