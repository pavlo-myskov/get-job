from django.db import models
from django.urls import reverse

IRELAND_COUNTIES = (
    ("DUBLIN", "Dublin"),
    ("DUBLIN_CITY_CENTRE", "Dublin City Centre"),
    ("DUBLIN_NORTH", "Dublin North"),
    ("DUBLIN_SOUTH", "Dublin South"),
    ("DUBLIN_WEST", "Dublin West"),
    ("CARLOW", "Carlow"),
    ("CAVAN", "Cavan"),
    ("CLARE", "Clare"),
    ("CORK", "Cork"),
    ("DONEGAL", "Donegal"),
    ("GALWAY", "Galway"),
    ("KERRY", "Kerry"),
    ("KILDARE", "Kildare"),
    ("KILKENNY", "Kilkenny"),
    ("LAOIS", "Laois"),
    ("LEITRIM", "Leitrim"),
    ("LIMERICK", "Limerick"),
    ("LONGFORD", "Longford"),
    ("LOUTH", "Louth"),
    ("MAYO", "Mayo"),
    ("MEATH", "Meath"),
    ("MONAGHAN", "Monaghan"),
    ("OFFALY", "Offaly"),
    ("ROSCOMMON", "Roscommon"),
    ("SLIGO", "Sligo"),
    ("TIPPERARY", "Tipperary"),
    ("WATERFORD", "Waterford"),
    ("WESTMEATH", "Westmeath"),
    ("WEXFORD", "Wexford"),
    ("WICKLOW", "Wicklow"),
    ("NORTHERN_IRELAND", "Northern Ireland"),
    ("UK", "UK"),
    ("EUROPE", "Europe"),
    ("WORLDWIDE", "Worldwide"),
)

JOB_TYPES = (
    ("FULL_TIME", "Full Time"),
    ("PART_TIME", "Part Time"),
    ("CONTRACT", "Contract"),
    ("PERMANENT", "Permanent"),
    ("TEMPORARY", "Temporary"),
    ("APPRENTICESHIP", "Apprenticeship"),
    ("VOLUNTEER", "Volunteer"),
)

JOB_LOCATIONS = (
    ("ON_SITE", "On Site"),
    ("REMOTE", "Remote"),
    ("HYBRID", "Hybrid"),
)

JOB_POST_STATUS = (
    ("R", "In review"),
    ("A", "Active"),
    ("W", "Withdrawn"),
    ("C", "Closed"),
)


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
        choices=IRELAND_COUNTIES, max_length=50, blank=False
    )
    job_location = models.CharField(
        max_length=50, choices=JOB_LOCATIONS, blank=False
    )
    job_type = models.CharField(choices=JOB_TYPES, max_length=50, blank=False)
    salary = models.CharField(max_length=50, default="Negotiable", blank=False)
    experience = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=JOB_POST_STATUS, max_length=50, default="R"
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
