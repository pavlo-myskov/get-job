from django.db import models
from django.urls import reverse


class IrelandAreas(models.TextChoices):
    REPUBLIC_OF_IRELAND = "REPUBLIC_OF_IRELAND", "Republic of Ireland"
    DUBLIN_CITY = "DUBLIN_CITY", "Dublin"
    DUBLIN_CITY_CENTRE = "DUBLIN_CITY_CENTRE", "Dublin City Centre"
    DUBLIN_NORTH = "DUBLIN_NORTH", "Dublin North"
    DUBLIN_SOUTH = "DUBLIN_SOUTH", "Dublin South"
    DUBLIN_WEST = "DUBLIN_WEST", "Dublin West"
    DUBLIN_COUNTY = "DUBLIN_COUNTY", "co. Dublin"
    CARLOW = "CARLOW", "co. Carlow"
    CAVAN = "CAVAN", "co. Cavan"
    CLARE = "CLARE", "co. Clare"
    CORK_CITY = "CORK_CITY", "Cork"
    CORK_COUNTY = "CORK_COUNTY", "co. Cork"
    DONEGAL = "DONEGAL", "co. Donegal"
    GALWAY_CITY = "GALWAY_CITY", "Galway"
    GALWAY_COUNTY = "GALWAY_COUNTY", "co. Galway"
    KERRY = "KERRY", "co. Kerry"
    KILDARE = "KILDARE", "co. Kildare"
    KILKENNY_CITY = "KILKENNY_CITY", "Kilkenny"
    KILKENNY_COUNTY = "KILKENNY_COUNTY", "co. Kilkenny"
    LAOIS = "LAOIS", "co. Laois"
    LEITRIM = "LEITRIM", "co. Leitrim"
    LIMERICK_CITY = "LIMERICK_CITY", "Limerick"
    LIMERICK_COUNTY = "LIMERICK_COUNTY", "co. Limerick"
    LONGFORD = "LONGFORD", "co. Longford"
    LOUTH = "LOUTH", "co. Louth"
    MAYO = "MAYO", "co. Mayo"
    MEATH = "MEATH", "co. Meath"
    MONAGHAN = "MONAGHAN", "co. Monaghan"
    OFFALY = "OFFALY", "co. Offaly"
    ROSCOMMON = "ROSCOMMON", "co. Roscommon"
    SLIGO = "SLIGO", "co. Sligo"
    TIPPERARY = "TIPPERARY", "co. Tipperary"
    WATERFORD_CITY = "WATERFORD_CITY", "Waterford"
    WATERFORD_COUNTY = "WATERFORD_COUNTY", "co. Waterford"
    WESTMEATH = "WESTMEATH", "co. Westmeath"
    WEXFORD = "WEXFORD", "co. Wexford"
    WICKLOW = "WICKLOW", "co. Wicklow"
    NORTHERN_IRELAND = "NORTHERN_IRELAND", "Northern Ireland"
    UK = "UK", "UK"
    EUROPE = "EUROPE", "Europe"
    WORLDWIDE = "WORDLWIDE", "Worldwide"


class Vacancy(models.Model):

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
        choices=IrelandAreas.choices, max_length=50, blank=False
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
