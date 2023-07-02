from django.db.models import Q
from django.db.models import QuerySet
from django.db.models import Case, When, BooleanField

from users.models import User
from .models import Vacancy, Areas, IRELAND_AREAS, DUBLIN_AREAS


def filter_jobs(search_data: dict) -> QuerySet:
    """Search for vacancies with the provided search data with Q objects
    :param search_data: cleaned search data from the search form
    without empty fields
    :return: Vacancy queryset
    """
    query = Q()
    # change title to title__icontains
    # to search for case insensitive title
    if search_data.get("title"):
        query &= Q(title__icontains=search_data["title"])

    if search_data.get("area"):
        area = search_data["area"]
        # change area to area__in if Areas.IRELAND is provided
        # to search in by irish areas only
        if area == Areas.IRELAND:
            query &= Q(area__in=IRELAND_AREAS)
        # search in dublin areas only if DUBLIN_CITY is provided
        elif area == Areas.DUBLIN_CITY:
            query &= Q(area__in=DUBLIN_AREAS)
        else:
            query &= Q(area=area)

    if search_data.get("job_location"):
        query &= Q(job_location=search_data["job_location"])

    if search_data.get("job_type"):
        query &= Q(job_type=search_data["job_type"])

    # search for vacancies with the provided search data
    job_list = Vacancy.objects.active().filter(query).distinct()

    return job_list


def annotate_saved_jobs(queryset: QuerySet, request) -> QuerySet:
    """Annotate the vacancies with is_saved field
    if user is authenticated and is a jobseeker.
    :is_saved: is True if the vacancy is in the jobseeker's favorites.

    :param queryset: Vacancy queryset
    :param request: request object
    :return: annotated queryset or the original queryset if the user is not
    authenticated or is not a jobseeker
    """
    if (
        request.user.is_authenticated
        and request.user.role == User.Role.JOBSEEKER
    ):
        profile = request.user.jobseekerprofile

        # get the ids of the saved vacancies
        saved_ids = profile.favorites.values_list("id", flat=True)
        # set is_saved to True if the vacancy id is in saved_ids
        queryset = queryset.annotate(
            is_saved=Case(
                When(id__in=saved_ids, then=True),
                default=False,
                output_field=BooleanField(),
            )
        )

    return queryset
