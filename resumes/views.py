import re
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.db.models import QuerySet

from users.models import User
from .models import Resume
from .forms import ResumeSearchForm


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


class ResumeListView(ListView):
    paginate_by = 6

    def get_queryset(self):
        """
        Search for aproved resumes by title if search query is provided,
        otherwise return all approved resumes (even if empty query is provided)
        """
        # get search query from search panel if it is provided,
        # otherwise prepopulate the search form with the session data
        # if session data is also not provided return all approved resumes
        if self.request.GET:
            self.form = ResumeSearchForm(self.request.GET)
        elif self.request.session.get("resume_search_query"):
            self.form = ResumeSearchForm(
                self.request.session.get("resume_search_query")
            )
        else:
            self.form = ResumeSearchForm()
            return Resume.objects.active()

        # if form is valid, search for resumes
        if self.form.is_valid():
            # filter only non-empty fields
            search_data = {
                key: value
                for key, value in self.form.cleaned_data.items()
                if value
            }
            # if search data is empty:
            # - return unboud form
            # - update session with empty search query
            # - return all approved resumes
            if not search_data:
                self.form = ResumeSearchForm()
                self.request.session["resume_search_query"] = {}
                resume_list = Resume.objects.active()
            else:
                # update session with the new search query if it is provided
                if self.request.GET:
                    self.request.session[
                        "resume_search_query"
                    ] = self.form.cleaned_data

                resume_list = filter_resumes(search_data)
        else:
            # if form is not valid, return an empty queryset
            resume_list = Resume.objects.none()
        return resume_list

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        context = super().get_context_data(**kwargs)
        context["form"] = self.form

        # add age error messages to the context if they exist
        if "min_age" in self.form.errors or "max_age" in self.form.errors:
            context["age_error"] = "Age must be between 18 and 66 years"

        # create a new instance of the form to be used in the navbar
        context["nav_form"] = ResumeSearchForm(auto_id=False)

        # elided pagination
        # https://docs.djangoproject.com/en/3.2/_modules/django/core/paginator/#Paginator.get_elided_page_range
        page_obj = context["page_obj"]
        custom_page_range = page_obj.paginator.get_elided_page_range(
            number=page_obj.number, on_each_side=1, on_ends=1
        )
        context["custom_page_range"] = custom_page_range
        return context


class ResumeDetailView(DetailView):

    def get_queryset(self):
        # TODO: add test
        """Return all active resumes and all resumes of the owner
        if the user is authenticated as a jobseeker"""
        query = Q()
        if (
            self.request.user.is_authenticated
            and self.request.user.role == User.Role.JOBSEEKER
        ):
            query = Q(jobseeker__id=self.request.user.pk)

        queryset = Resume.objects.filter(
            query | Q(status=Resume.ResumePublishStatus.ACTIVE)
        )
        return queryset

    def get_context_data(self, **kwargs):
        """Add search form to the context for navbar search bar"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = ResumeSearchForm(auto_id=False)
        return context
