from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView

from jobseeker.views import JobseekerRequiredMixin

from .models import Vacancy, Areas, IRELAND_AREAS, DUBLIN_AREAS
from .forms import SearchForm


def filter_jobs(search_data) -> QuerySet:
    """Search for vacancies with the provided search data with Q objects"""
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


class JobListView(ListView):
    context_object_name = "job_list"
    paginate_by = 6

    def get_queryset(self):
        """
        Search for aproved jobs by title if search query is provided,
        otherwise return all approved jobs (even if empty query is provided)
        """
        # get search query from search panel if it is provided,
        # otherwise prepopulate the search form with the session data
        # if session data is also not provided return all approved jobs
        if self.request.GET:
            self.form = SearchForm(self.request.GET)
        elif self.request.session.get("job_search_query"):
            self.form = SearchForm(
                self.request.session.get("job_search_query")
            )
        else:
            self.form = SearchForm()
            return Vacancy.objects.filter(status=Vacancy.JobPostStatus.ACTIVE)

        # if form is valid, search for vacancies
        if self.form.is_valid():
            # get search fields from cleaned_data if they are not empty
            search_data = {
                key: value
                for key, value in self.form.cleaned_data.items()
                if value
            }

            # if search data is empty:
            # - return unboud form
            # - update session with empty search query
            # - return all approved jobs
            if not search_data:
                self.form = SearchForm()
                self.request.session["job_search_query"] = {}
                job_list = Vacancy.objects.active()
            else:
                # update session with the new search query if it is provided
                if self.request.GET:
                    self.request.session[
                        "job_search_query"
                    ] = self.form.cleaned_data

                job_list = filter_jobs(search_data)
        else:
            # if form is not valid, return an empty queryset
            job_list = Vacancy.objects.none()

        return job_list

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        # create a new instance of the form to be used in the navbar
        context["nav_form"] = SearchForm(auto_id=False)

        # elided pagination
        # https://docs.djangoproject.com/en/3.2/_modules/django/core/paginator/#Paginator.get_elided_page_range
        page_obj = context["page_obj"]
        custom_page_range = page_obj.paginator.get_elided_page_range(
            number=page_obj.number, on_each_side=1, on_ends=1
        )
        context["custom_page_range"] = custom_page_range
        return context


class JobDetailView(DetailView):
    # get only active vacancies
    queryset = Vacancy.objects.active()

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        context = super().get_context_data(**kwargs)
        # create a new instance of the form to be used in the navbar
        context["nav_form"] = SearchForm(auto_id=False)

        return context


class JobSaveToggle(LoginRequiredMixin, JobseekerRequiredMixin, View):
    """Toggle save/unsave job for the current jobseeker"""

    http_method_names = ["post"]  # only POST requests are allowed

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        vacancy = get_object_or_404(Vacancy, pk=pk)
        profile = request.user.jobseekerprofile
        if profile.favorites.filter(id=vacancy.id).exists():
            profile.favorites.remove(vacancy.id)
            result = "unsaved"
        else:
            profile.favorites.add(vacancy.id)
            result = "saved"

        return JsonResponse({"result": "success", "action": result})
