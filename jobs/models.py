from django.db import models
from django.urls import reverse


class IrelandCounties(models.TextChoices):
    DUBLIN = "DUBLIN", "Dublin"
    DUBLIN_CITY_CENTRE = "DUBLIN_CITY_CENTRE", "Dublin City Centre"
    DUBLIN_NORTH = "DUBLIN_NORTH", "Dublin North"
    DUBLIN_SOUTH = "DUBLIN_SOUTH", "Dublin South"
    DUBLIN_WEST = "DUBLIN_WEST", "Dublin West"
    CARLOW = "CARLOW", "Carlow"
    CAVAN = "CAVAN", "Cavan"
    CLARE = "CLARE", "Clare"
    CORK = "CORK", "Cork"
    DONEGAL = "DONEGAL", "Donegal"
    GALWAY = "GALWAY", "Galway"
    KERRY = "KERRY", "Kerry"
    KILDARE = "KILDARE", "Kildare"
    KILKENNY = "KILKENNY", "Kilkenny"
    LAOIS = "LAOIS", "Laois"
    LEITRIM = "LEITRIM", "Leitrim"
    LIMERICK = "LIMERICK", "Limerick"
    LONGFORD = "LONGFORD", "Longford"
    LOUTH = "LOUTH", "Louth"
    MAYO = "MAYO", "Mayo"
    MEATH = "MEATH", "Meath"
    MONAGHAN = "MONAGHAN", "Monaghan"
    OFFALY = "OFFALY", "Offaly"
    ROSCOMMON = "ROSCOMMON", "Roscommon"
    SLIGO = "SLIGO", "Sligo"
    TIPPERARY = "TIPPERARY", "Tipperary"
    WATERFORD = "WATERFORD", "Waterford"
    WESTMEATH = "WESTMEATH", "Westmeath"
    WEXFORD = "WEXFORD", "Wexford"
    WICKLOW = "WICKLOW", "Wicklow"
    NORTHERN_IRELAND = "NORTHERN_IRELAND", "Northern Ireland"
    UK = "UK", "UK"
    EUROPE = "EUROPE", "Europe"
    WORLDWIDE = "WORDLWIDE", "Worldwide"


class JobTypes(models.TextChoices):
    FULL_TIME = "FULL_TIME", "Full Time"
    PART_TIME = "PART_TIME", "Part Time"
    CONTRACT = "CONTRACT", "Contract"
    PERMANENT = "PERMANENT", "Permanent"
    TEMPORARY = "TEMPORARY", "Temporary"
    APPRENTICESHIP = "APPRENTICESHIP", "Apprenticeship"
    VOLUNTEER = "VOLUNTEER", "Volunteer"


class JobLocations(models.TextChoices):
    ON_SITE = "ON_SITE", "On Site"
    REMOTE = "REMOTE", "Remote"
    HYBRID = "HYBRID", "Hybrid"


class JobPostStatus(models.TextChoices):
    IN_REVIEW = "IN_REVIEW", "In Review"
    ACTIVE = "ACTIVE", "Active"
    WITHDRAWN = "WITHDRAWN", "Withdrawn"
    CLOSED = "CLOSED", "Closed"


class Vacancy(models.Model):
    title = models.CharField(max_length=255, blank=False)
    """
    # TODO: add FKs to Employer and Company models
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, related_name="vaccancies"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="vaccancies"
    )
    """
    body = models.TextField(blank=False)
    area = models.CharField(
        choices=IrelandCounties.choices, max_length=50, blank=False
    )
    job_location = models.CharField(
        max_length=50, choices=JobLocations.choices, blank=False
    )
    job_type = models.CharField(
        choices=JobTypes.choices, max_length=50, blank=False
    )
    salary = models.CharField(max_length=50, default="Negotiable", blank=False)
    experience = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=JobPostStatus.choices,
        max_length=50,
        default=JobPostStatus.IN_REVIEW,
    )

    class Meta:
        # the vaccancies will be ordered by the date they were created,
        # with the most recent ones at the top
        ordering = ["-created_on"]
        verbose_name_plural = "vacancies"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("jobs:vacancy_detail", args=[str(self.id)])
