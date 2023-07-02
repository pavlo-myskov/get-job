from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView

from jobseeker.views import JobseekerRequiredMixin

from .utils import annotate_saved_jobs, filter_jobs
from .models import Vacancy
from .forms import SearchForm


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
            job_list = Vacancy.objects.filter(
                status=Vacancy.JobPostStatus.ACTIVE
            )
            return annotate_saved_jobs(job_list, self.request)

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

        return annotate_saved_jobs(job_list, self.request)

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

    def get_queryset(self):
        queryset = super().get_queryset()
        return annotate_saved_jobs(queryset, self.request)

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
            is_saved = False
            success_message = "The job has been removed from saved jobs."
        else:
            profile.favorites.add(vacancy.id)
            is_saved = True
            success_message = "The job has been saved."

        return JsonResponse(
            {"is_saved": is_saved, "successMsg": success_message}
        )
