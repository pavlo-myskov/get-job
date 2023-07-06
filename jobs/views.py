from django.contrib import messages
from django.forms import BaseForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from employer.views import EmployerRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from jobseeker.views import JobseekerRequiredMixin

from .utils import annotate_jobs, filter_jobs
from .models import Application, Vacancy
from .forms import ApplicationForm, JobCreateForm, SearchForm
from resumes.models import Resume


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
            return annotate_jobs(job_list, self.request)

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

        return annotate_jobs(job_list, self.request)

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
        return annotate_jobs(queryset, self.request)

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        context = super().get_context_data(**kwargs)
        # create a new instance of the form to be used in the navbar
        context["nav_form"] = SearchForm(auto_id=False)

        return context


class JobSaveToggle(JobseekerRequiredMixin, View):
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


class JobApplyView(JobseekerRequiredMixin, CreateView):
    form_class = ApplicationForm
    template_name = "jobs/job_apply.html"
    success_message = (
        "You have applied for the job successfully."
        " Wait for the employer to contact you."
    )

    def get_form_kwargs(self):
        """Passes the request object to the form class."""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        """Save the jobseeker and the job to the application"""
        form.instance.applicant = self.request.user.jobseekerprofile
        form.instance.vacancy = get_object_or_404(
            Vacancy,
            pk=self.kwargs.get("pk"),
            status=Vacancy.JobPostStatus.ACTIVE,
        )
        # check if the applicant has already applied for the job
        if Application.objects.filter(
            applicant=form.instance.applicant, vacancy=form.instance.vacancy
        ).exists():
            form.add_error(
                None,
                "You have already applied for this job. "
                "Please wait for the employer to contact you.",
            )
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the job detail page"""
        return reverse("job_detail", kwargs={"pk": self.kwargs.get("pk")})

    def get_context_data(self, **kwargs):
        """Add search form, vacancy and resumes to the context"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = SearchForm(auto_id=False)
        context["vacancy"] = get_object_or_404(
            Vacancy,
            pk=self.kwargs.get("pk"),
            status=Vacancy.JobPostStatus.ACTIVE,
        )
        context["are_resumes_available"] = self.request.user.resumes.filter(
            status=Resume.ResumePublishStatus.ACTIVE
        ).exists()
        return context


class JobCreateView(EmployerRequiredMixin, SuccessMessageMixin, CreateView):
    model = Vacancy
    form_class = JobCreateForm
    template_name_suffix = "_create_form"
    success_message = (
        "Your vacancy has been created and is "
        "<span class='text-info'>pending approval</span>"
    )

    def test_func(self):
        """Check if the user has less or equal than 5 vacancies"""
        self.employer_test = super().test_func()
        self.has_less_6_vacancies = (
            self.request.user.vacancies.all().count() <= 4
        )
        return self.employer_test and self.has_less_6_vacancies

    def handle_no_permission(self):
        """Redirect to the vacancy list page and show an alert,
        if the user has more than 5 vacancies;
        if the user is not an employer, redirect to the specific 403 page"""
        # redirect to login page if the user is not authenticated
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        if self.employer_test and not self.has_less_6_vacancies:
            messages.error(
                self.request,
                "The maximum number of vacancies has been reached. ",
                extra_tags="modal",
            )
            return HttpResponseRedirect(reverse_lazy("my_vacancies"))

        return super().handle_no_permission()

    def get_success_url(self):
        """Redirect to the 'next' url if it exists,
        otherwise to the vacancy detail page"""
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        return reverse("my_job_detail", args=(self.object.id,))

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """Save the current user as a employer-owner of the vacancy"""
        form.instance.employer = self.request.user
        return super().form_valid(form)
