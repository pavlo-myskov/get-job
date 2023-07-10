from django.template.loader import render_to_string
from django.core import serializers
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, CreateView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages

from allauth.account.utils import get_next_redirect_url
from jobportal.base_views import ResumeSnapshotView, VacancySnapshotView
from jobs.models import Application, Vacancy
from resumes.utils import annotate_offered_resumes, annotate_resumes

from users.models import User

from resumes.models import Resume
from resumes.forms import ResumeSearchForm

from .models import EmployerProfile, JobOffer
from .forms import EmployerProfileForm, OfferForm


class EmployerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        """Check if the user is a Employer"""
        return self.request.user.role == User.Role.EMPLOYER

    def handle_no_permission(self):
        """
        If the request is AJAX, return a JSON response with
        the HTML of the 403 page.

        Redirect to the specific page based on the user's authentication
        status and role:
        - Redirect to the login page if the user is not authenticated.
        - Display the 403 employer page if the role is not EMPLOYER.
        - Otherwise, display the default 403 page.
        """
        if self.request.is_ajax():
            error_403_html = render_to_string("errors/403.html")
            return JsonResponse(
                {"error": "Forbidden", "html_page": error_403_html},
                status=403,
            )
        if not self.request.user.is_authenticated:
            message = "Sign in or create an account"
            " as an Employer to access this page"
            messages.add_message(self.request, messages.WARNING, message)
            return super().handle_no_permission()
        elif self.request.user.role != User.Role.EMPLOYER:
            return render(self.request, "errors/employer_403.html", status=403)
        else:
            return super().handle_no_permission()


class HomeView(ListView):
    # object name that will be used in the template
    context_object_name = "resume_list"
    # get only first 4 active resumes
    queryset = Resume.objects.active()[:4]
    template_name = "employer/home.html"

    def get_queryset(self):
        """Annotate the resumes with is_saved field
        if user is authenticated and is a employer"""
        queryset = super().get_queryset()
        return annotate_resumes(queryset, self.request)

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        context = super().get_context_data(**kwargs)

        # prepopulate the search form with the session data
        search_query = self.request.session.get("resume_search_query")
        if search_query and search_query.get("keywords"):
            form = ResumeSearchForm(
                {"keywords": search_query.get("keywords")}, auto_id=False
            )
        else:
            form = ResumeSearchForm(auto_id=False)

        context["form"] = form
        context["nav_form"] = ResumeSearchForm(auto_id=False)
        return context


class EmployerProfileDetailView(EmployerRequiredMixin, DetailView):
    model = EmployerProfile
    template_name = "employer/profile.html"
    context_object_name = "profile"

    def test_func(self):
        """Allow only the owner to view the profile"""
        employer_test = super().test_func()
        return employer_test and self.request.user == self.get_object().user

    def get_object(self, queryset=None):
        """Return the employer profile for the current user"""
        return self.request.user.employerprofile

    def get_context_data(self, **kwargs):
        """Add search form and back URL to the context"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = ResumeSearchForm(auto_id=False)
        return context


class EmployerProfileUpdateView(
    EmployerRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = EmployerProfile
    form_class = EmployerProfileForm
    template_name = "employer/profile_update.html"
    success_message = "Your profile has been updated successfully"

    def test_func(self):
        """Allow only the owner to update the profile"""
        employer_test = super().test_func()
        return employer_test and self.request.user == self.get_object().user

    def get_object(self, queryset=None):
        """Return the employer profile for the current user"""
        return self.request.user.employerprofile

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.
        - Redirect to the `next` parameter if it exists
        - Otherwise, redirect to the employer profile page
        """
        # get next url using allauth's get_next_redirect_url,
        # allows to perform checks to prevent redirecting to other sites
        next_url = get_next_redirect_url(self.request)
        if next_url:
            return next_url
        else:
            return reverse("employer_profile")


class FavoriteResumeList(EmployerRequiredMixin, ListView):
    template_name = "employer/favorite_resumes.html"
    context_object_name = "favorite_list"

    def get_queryset(self):
        favorites = self.request.user.employerprofile.favorites.all()
        return annotate_offered_resumes(favorites, self.request)

    def get_context_data(self, **kwargs):
        """Add search form and back URL to the context"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = ResumeSearchForm(auto_id=False)
        return context


class JobOfferView(EmployerRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = OfferForm
    template_name = "employer/job_offer.html"
    success_message = "Your offer has been sent successfully. "

    def get_form_kwargs(self):
        """Passes the request object to the form class."""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        """Save the employer and the resume to the offer"""
        form.instance.employer = self.request.user
        form.instance.resume = get_object_or_404(
            Resume,
            pk=self.kwargs.get("pk"),
            status=Resume.ResumePublishStatus.ACTIVE,
        )
        # check if the employer has already sent an offer to the jobseeker with
        # the same vacancy
        if JobOffer.objects.filter(
            employer=form.instance.employer,
            resume=form.instance.resume,
            vacancy=form.instance.vacancy,
        ).exists():
            my_job_offers_url = reverse("my_job_offers")
            form.add_error(
                None,
                "You have already sent an offer to this jobseeker for "
                "selected vacancy. <br>Please, check your "
                f"<a href='{my_job_offers_url}'>Job Offers</a> list.",
            )
            return super().form_invalid(form)
        # check if the jobseeker has already applied to the selected vacancy
        # with the same resume
        elif Application.objects.filter(
            resume=form.instance.resume,
            vacancy=form.instance.vacancy,
        ).exists():
            # TODO: add link to the applicants list
            applicants_url = reverse("employer_home")
            form.add_error(
                None,
                "This jobseeker has already applied to selected vacancy "
                "with current resume. <br>Please, check "
                f"<a class='{applicants_url}'>Applicants</a> list.",
            )
            return super().form_invalid(form)

        # serialize vacancy and resume instances to JSON and
        # save them to the offer instance
        form.instance.vacancy_snapshot = serializers.serialize(
            "json", [form.instance.vacancy]
        )
        form.instance.resume_snapshot = serializers.serialize(
            "json", [form.instance.resume]
        )

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the resume search page"""
        pk = self.kwargs.get("pk")
        url = reverse("resume_search")
        return f"{url}#{pk}"

    def get_context_data(self, **kwargs):
        """Add search form, vacancy and resumes to the context"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = ResumeSearchForm(auto_id=False)
        context["resume"] = get_object_or_404(
            Resume,
            pk=self.kwargs.get("pk"),
            status=Resume.ResumePublishStatus.ACTIVE,
        )
        context["are_jobs_available"] = self.request.user.vacancies.filter(
            status=Vacancy.JobPostStatus.ACTIVE,
        ).exists()
        return context


class MyJobOfferList(EmployerRequiredMixin, ListView):
    template_name = "employer/my_job_offers.html"

    def get_queryset(self):
        job_offers = self.request.user.job_offers.all()
        return job_offers

    def get_context_data(self, **kwargs):
        """Add search form and back URL to the context"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = ResumeSearchForm(auto_id=False)
        return context


class JobOfferResumeSnapshotView(EmployerRequiredMixin, ResumeSnapshotView):
    model = JobOffer

    def test_func(self):
        """Allow only the owner to view the job offer resume snapshot"""
        employer_test = super().test_func()
        return (
            employer_test and self.request.user == self.get_object().employer
        )


class JobOfferVacancySnapshotView(EmployerRequiredMixin, VacancySnapshotView):
    model = JobOffer

    def test_func(self):
        """Allow only the owner to view the job offer vacancy snapshot"""
        employer_test = super().test_func()
        return (
            employer_test and self.request.user == self.get_object().employer
        )
