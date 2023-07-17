from django.core import serializers
from django.contrib import messages
from django.db import transaction
from django.forms import BaseForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.db.models import Count
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from employer.models import JobOffer
from employer.views import EmployerRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from jobportal.base_views import (
    JobSearchFormMixin,
    RelatedUserRequiredMixin,
    ResumeSearchFormMixin,
    ResumeSnapshotView,
    VacancySnapshotView,
)
from jobseeker.views import JobseekerRequiredMixin
from users.models import User

from .utils import annotate_jobs, filter_jobs
from .models import Application, Vacancy
from .forms import ApplicationForm, JobCreateForm, JobSearchForm
from resumes.models import Resume


class JobListView(JobSearchFormMixin, ListView):
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
            self.form = JobSearchForm(self.request.GET)
        elif self.request.session.get("job_search_query"):
            self.form = JobSearchForm(
                self.request.session.get("job_search_query")
            )
        else:
            self.form = JobSearchForm()
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
                self.form = JobSearchForm()
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

        # elided pagination
        # https://docs.djangoproject.com/en/3.2/_modules/django/core/paginator/#Paginator.get_elided_page_range
        page_obj = context["page_obj"]
        custom_page_range = page_obj.paginator.get_elided_page_range(
            number=page_obj.number, on_each_side=1, on_ends=1
        )
        context["custom_page_range"] = custom_page_range
        return context


class JobDetailView(JobSearchFormMixin, DetailView):
    # get only active vacancies
    queryset = Vacancy.objects.active()

    def get_queryset(self):
        queryset = super().get_queryset()
        return annotate_jobs(queryset, self.request)


class MyJobListView(EmployerRequiredMixin, ResumeSearchFormMixin, ListView):
    model = Vacancy
    template_name = "jobs/my_jobs.html"

    def get_queryset(self):
        # TODO: add test
        """Return all jobs of the owner,
        ordered by status, updated_on.
        Example: IN_REVIEW on top and with the latest updated_on date"""
        return Vacancy.objects.filter(employer=self.request.user).order_by(
            "-status",
            "-updated_on",
        )

    def get_context_data(self, **kwargs):
        """Add to the context:
        - tooltips for tooltip status icons
        - search form for navbar search bar
        """
        context = super().get_context_data(**kwargs)

        # add status tooltips to the context
        tooltips = {
            Vacancy.JobPostStatus.ACTIVE: "This job is visible"
            " to jobseekers",
            Vacancy.JobPostStatus.IN_REVIEW: "This job is pending" " approval",
            Vacancy.JobPostStatus.REJECTED: "This job contains"
            " inappropriate content or does not meet the requirements",
            Vacancy.JobPostStatus.CLOSED: "This job is not visible and"
            " cannot be edited",
        }
        context["tooltips"] = tooltips
        return context


class MyVacancyDetailView(
    EmployerRequiredMixin, ResumeSearchFormMixin, DetailView
):
    model = Vacancy
    template_name = "jobs/my_vacancy_detail.html"

    def get_queryset(self):
        # TODO: add test
        """Return all jobs of the owner"""
        return Vacancy.objects.filter(employer=self.request.user)


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
            return HttpResponseRedirect(reverse("my_jobs"))

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


class JobUpdateView(EmployerRequiredMixin, SuccessMessageMixin, UpdateView):
    # TODO: add test
    model = Vacancy
    form_class = JobCreateForm
    template_name_suffix = "_update_form"
    success_message = (
        "Your vacancy has been updated and is "
        "<span class='text-info'>pending approval</span>"
    )

    def test_func(self):
        """Allow only the owner to update the vacancy,
        if the vacancy is not closed"""
        self.employer_test = super().test_func()
        return (
            self.employer_test
            and self.request.user == self.get_object().employer
            and self.get_object().status != Vacancy.JobPostStatus.CLOSED
        )

    def get_success_url(self):
        """Redirect to the vacancy detail page"""
        return reverse("my_job_detail", kwargs={"pk": self.get_object().pk})

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """Set the status of the vacancy to IN_REVIEW"""
        form.instance.status = Vacancy.JobPostStatus.IN_REVIEW
        return super().form_valid(form)


class JobCloseView(
    EmployerRequiredMixin,
    SingleObjectMixin,
    View,
):
    # TODO: add test
    http_method_names = ["post"]  # only POST requests are allowed
    model = Vacancy

    def test_func(self):
        # TODO: redirection tests
        """Allow only the owner to close the job,
        if the job is not closed yet"""
        self.employer_test = super().test_func()
        return (
            self.employer_test
            and self.request.user == self.get_object().employer
            and self.get_object().status != Vacancy.JobPostStatus.CLOSED
        )

    # allows save object only if the transaction is successful
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Set the status of the job to CLOSED"""
        self.object = self.get_object()
        self.object.status = Vacancy.JobPostStatus.CLOSED
        self.object.save()
        messages.success(self.request, "Your job has been closed")
        return HttpResponseRedirect(reverse("my_jobs"))


class JobOpenView(
    EmployerRequiredMixin,
    SingleObjectMixin,
    View,
):
    # TODO: add test
    http_method_names = ["post"]  # only POST requests are allowed
    model = Vacancy

    def test_func(self):
        # TODO: redirection tests
        """Allow only the owner to open the job,
        if the job is closed"""
        self.employer_test = super().test_func()
        return (
            self.employer_test
            and self.request.user == self.get_object().employer
            and self.get_object().status == Vacancy.JobPostStatus.CLOSED
        )

    # allows save object only if the transaction is successful
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Set the status of the job to IN_REVIEW"""
        self.object = self.get_object()
        self.object.status = Vacancy.JobPostStatus.IN_REVIEW
        self.object.save()
        messages.success(
            self.request,
            "Your job has been opened and is awaiting approval",
        )
        return HttpResponseRedirect(reverse("my_jobs"))


class JobDeleteView(EmployerRequiredMixin, DeleteView):
    model = Vacancy
    template_name = "jobs/my_jobs.html"
    success_message = "Your job has been permanently deleted"
    success_url = reverse_lazy("my_jobs")

    def test_func(self):
        """Allow only the owner to delete the job"""
        self.employer_test = super().test_func()
        return (
            self.employer_test
            and self.request.user == self.get_object().employer
        )

    def delete(self, request, *args, **kwargs):
        """Add success message to the delete view"""
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


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


class JobApplyView(
    JobseekerRequiredMixin, JobSearchFormMixin, SuccessMessageMixin, CreateView
):
    form_class = ApplicationForm
    template_name = "jobs/job_apply.html"
    success_message = "You have applied for the job successfully."

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
        # with the same resume
        if Application.objects.filter(
            applicant=form.instance.applicant,
            vacancy=form.instance.vacancy,
            resume=form.instance.resume,
        ).exists():
            job_applications_url = reverse("applied_jobs")
            form.add_error(
                None,
                "You have already applied for this job "
                "with selected resume. <br>Please check your "
                f"<a href='{job_applications_url}'>Job Applications</a>",
            )
            return super().form_invalid(form)
        # check if the employer has already sent a job offer to the applicant
        # with the selected resume for the current job
        elif JobOffer.objects.filter(
            resume=form.instance.resume,
            vacancy=form.instance.vacancy,
        ).exists():
            job_invitations_url = reverse("jobseeker_home")
            form.add_error(
                None,
                "You have already received a job offer for this job "
                "with selected resume. <br>Please check your "
                f"<a href='{job_invitations_url}'>Job Invitations</a>",
            )
            return super().form_invalid(form)

        # serialize vacancy and resume instances to JSON and
        # save them to the application instance
        form.instance.vacancy_snapshot = serializers.serialize(
            "json", [form.instance.vacancy]
        )
        form.instance.resume_snapshot = serializers.serialize(
            "json", [form.instance.resume]
        )

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the job search page"""
        pk = self.kwargs.get("pk")
        url = reverse("job_search")
        return f"{url}#{pk}"

    def get_context_data(self, **kwargs):
        """Add search form, vacancy and resumes to the context"""
        context = super().get_context_data(**kwargs)
        context["vacancy"] = get_object_or_404(
            Vacancy,
            pk=self.kwargs.get("pk"),
            status=Vacancy.JobPostStatus.ACTIVE,
        )
        context["are_resumes_available"] = self.request.user.resumes.filter(
            status=Resume.ResumePublishStatus.ACTIVE
        ).exists()
        return context


class ApplicationMixin(RelatedUserRequiredMixin):
    """Mixin for the application snapshot views"""

    model = Application

    def test_func(self):
        """Allow only the related user to view
        the application snapshot"""
        user_test = super().test_func()
        if not user_test:
            return False

        # check if the user is the employer and
        # if he is the owner of the vacancy of the application
        # related to the resume snapshot
        if self.request.user.role == User.Role.EMPLOYER:
            return self.request.user == self.get_object().vacancy.employer
        elif self.request.user.role == User.Role.JOBSEEKER:
            return (
                self.request.user.jobseekerprofile
                == self.get_object().applicant
            )
        else:
            return False


class ApplicationResumeSnapshotView(ApplicationMixin, ResumeSnapshotView):
    pass


class ApplicationVacancySnapshotView(ApplicationMixin, VacancySnapshotView):
    pass


def annotate_applications_count(vacancies):
    """Annotate the vacancies with the number of applications
    for each vacancy"""
    return vacancies.annotate(
        num_applications=Count("applications", distinct=True)
    )


class ApplicantsList(EmployerRequiredMixin, ResumeSearchFormMixin, ListView):
    template_name = "employer/applicants_list.html"
    context_object_name = "vacancies"

    def get_queryset(self):
        """Return the list of employer's vacancies
        that have at least one application"""
        employer_vacancies = self.request.user.vacancies.filter(
            applications__isnull=False,
        ).distinct()

        return annotate_applications_count(employer_vacancies)
