import re
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet
from django.db.models import Q
from django.db.models import Case, When, BooleanField
from django.db.models import Subquery, OuterRef, DateTimeField
from resumes.models import Resume

from users.models import User


def get_keywords(search_data: dict) -> Q:
    """Extract keywords from search data with regex
    and return Q object with keywords"""

    # extract keywords from string using regex
    keywords_string = search_data.get("keywords", "").strip()
    keywords_list = re.findall(r"\w+", keywords_string)

    # "Search for multiple keywords over multiple columns in Django"
    # code snippet based on stackoverflow answer:
    # https://stackoverflow.com/a/43552495/20143678
    if keywords_list:
        keywords_obj = Q(occupation__icontains=keywords_list[0]) | Q(
            skills__icontains=keywords_list[0]
        )
        for keyword in keywords_list[1:]:
            keywords_obj.add(
                Q(occupation__icontains=keyword)
                | Q(skills__icontains=keyword),
                keywords_obj.connector,
            )
    else:
        keywords_obj = Q()

    return keywords_obj


def get_age_lookup(search_data: dict) -> Q:
    """Return lookup for age range from search data"""
    today = timezone.now().date()
    max_age = search_data.get("max_age", 66)
    min_age = search_data.get("min_age", 18)
    if min_age > max_age:
        min_age, max_age = max_age, min_age

    if min_age == max_age:
        # get all ages that are equal or older than 65
        if min_age == 66:
            dob_val = today - relativedelta(years=max_age - 1)
            lookup = Q(jobseeker__jobseekerprofile__dob__lte=dob_val)
        else:
            # if min_age and max_age are equal, search for exact age
            dob_val = today - relativedelta(years=min_age)
            lookup = Q(
                jobseeker__jobseekerprofile__dob__range=[
                    dob_val - relativedelta(years=1),
                    dob_val,
                ]
            )

    # if max_age is 66, search for all ages from min_age to 66 and older
    elif max_age == 66:
        startdate = today - relativedelta(years=min_age)
        lookup = Q(jobseeker__jobseekerprofile__dob__lte=startdate)

    else:
        # search for all ages from min_age to max_age(not including max_age)
        startdate = (
            today - relativedelta(years=max_age) + relativedelta(days=1)
        )
        enddate = today - relativedelta(years=min_age)
        lookup = Q(
            jobseeker__jobseekerprofile__dob__range=[startdate, enddate]
        )
    return lookup


def filter_resumes(search_data: dict) -> QuerySet:
    """
    Filter resumes by search data using Q objects
    """
    query = Q()
    # add Q objects to query if it is exist in search data
    if search_data.get("keywords"):
        query.add(get_keywords(search_data), query.connector)
    if search_data.get("experience"):
        query.add(
            Q(experience_duration__contains=search_data["experience"]),
            query.connector,
        )
    if search_data.get("gender"):
        # Lookups that span relationships
        query.add(
            Q(
                jobseeker__jobseekerprofile__gender__contains=search_data[  # noqa
                    "gender"
                ]
            ),
            query.connector,
        )
    if search_data.get("min_age") or search_data.get("max_age"):
        query.add(get_age_lookup(search_data), query.connector)
    # filter active resumes by search query
    # distinct() removes duplicate results
    resume_list = Resume.objects.active().filter(query).distinct()

    return resume_list


def annotate_saved_resumes(queryset: QuerySet, request) -> QuerySet:
    """Annotate the resumes with is_saved field.
    :is_saved: is True if the resume is in the employer's favorites.

    :param queryset: Resume queryset
    :param request: request object
    :return: annotated queryset
    """
    profile = request.user.employerprofile

    # get the ids of the saved resumes
    saved_ids = profile.favorites.values_list("id", flat=True)
    # set is_saved to True if the resume id is in saved_ids
    queryset = queryset.annotate(
        is_saved=Case(
            When(id__in=saved_ids, then=True),
            default=False,
            output_field=BooleanField(),
        )
    )

    return queryset


def annotate_resumes(queryset: QuerySet, request) -> QuerySet:
    """Main function to annotate the resumes with is_saved and is_hired.
    Annotate only if user is authenticated and is a employer otherwise
    return the original queryset.

    :return: annotated queryset or the original queryset
    """
    if (
        request.user.is_authenticated
        and request.user.role == User.Role.EMPLOYER
    ):
        queryset = annotate_saved_resumes(queryset, request)
        # TODO add:
        # queryset = annotate_hired_resumes(queryset, request)

    return queryset
