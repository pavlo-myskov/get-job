from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from allauth.account.utils import get_next_redirect_url

from jobs.models import Vacancy
from jobs.forms import SearchForm
from jobs.utils import annotate_applied_jobs, annotate_jobs

from users.models import User

from .models import JobseekerProfile
from .forms import JobseekerProfileForm


class JobseekerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        """Check if the user is a Jobseeker"""
        return self.request.user.role == User.Role.JOBSEEKER

    def handle_no_permission(self):
        """
        Redirect to the specific page based on the user's authentication
        status and role:
        - Redirect to the login page if the user is not authenticated.
        - Display the 403 jobseeker page if the role is not JOBSEEKER.
        - Otherwise, display the default 403 page.
        """
        if not self.request.user.is_authenticated:
            message = "Sign in or create an account"
            " as a Jobseeker to access this page"
            messages.add_message(self.request, messages.WARNING, message)
            return super().handle_no_permission()
        elif self.request.user.role != User.Role.JOBSEEKER:
            return render(
                self.request, "errors/jobseeker_403.html", status=403
            )
        else:
            return super().handle_no_permission()


class HomeView(ListView):
    # object name that will be used in the template
    context_object_name = "job_list"
    # get only first 4 active vacancies
    queryset = Vacancy.objects.active()[:4]
    template_name = "jobseeker/home.html"

    def get_queryset(self):
        """Annotate the vacancies with is_saved field
        if user is authenticated and is a jobseeker"""
        queryset = super().get_queryset()
        return annotate_jobs(queryset, self.request)

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        context = super().get_context_data(**kwargs)

        # prepopulate the search form with the session data
        search_query = self.request.session.get("job_search_query")
        if search_query and search_query.get("title"):
            form = SearchForm(
                {"title": search_query.get("title")}, auto_id=False
            )
        else:
            form = SearchForm(auto_id=False)

        context["form"] = form
        context["nav_form"] = SearchForm(auto_id=False)
        return context


class JobseekerProfileDetailView(JobseekerRequiredMixin, DetailView):
    model = JobseekerProfile
    template_name = "jobseeker/profile.html"
    context_object_name = "profile"

    def test_func(self):
        """Allow only the owner to view the profile"""
        jobseeker_test = super().test_func()
        return jobseeker_test and self.request.user == self.get_object().user

    def get_object(self, queryset=None):
        """Return the jobseeker profile for the current user"""
        return self.request.user.jobseekerprofile

    def get_context_data(self, **kwargs):
        """Add search form and back URL to the context"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = SearchForm(auto_id=False)
        return context


class JobseekerProfileUpdateView(
    JobseekerRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = JobseekerProfile
    form_class = JobseekerProfileForm
    template_name = "jobseeker/profile_update.html"
    success_message = "Your profile has been updated successfully"

    def test_func(self):
        """Allow only the owner to update the profile"""
        jobseeker_test = super().test_func()
        return jobseeker_test and self.request.user == self.get_object().user

    def get_object(self, queryset=None):
        """Return the jobseeker profile for the current user"""
        return self.request.user.jobseekerprofile

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.
        - Redirect to the `next` parameter if it exists
        - Otherwise, redirect to the jobseeker profile page
        """
        # get next url using allauth's get_next_redirect_url,
        # allows to perform checks to prevent redirecting to other sites
        next_url = get_next_redirect_url(self.request)
        if next_url:
            return next_url
        else:
            return reverse("jobseeker_profile")


class FavoriteJobList(JobseekerRequiredMixin, ListView):
    template_name = "jobseeker/favorite_jobs.html"
    context_object_name = "favorite_list"

    def get_queryset(self):
        favorites = self.request.user.jobseekerprofile.favorites.all()
        return annotate_applied_jobs(favorites, self.request)

    def get_context_data(self, **kwargs):
        """Add search form and back URL to the context"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = SearchForm(auto_id=False)
        return context


class AppliedJobList(JobseekerRequiredMixin, ListView):
    template_name = "jobseeker/applied_jobs.html"
    context_object_name = "applications"

    def get_queryset(self):
        applications = self.request.user.jobseekerprofile.applications.all()
        return applications

    def get_context_data(self, **kwargs):
        """Add search form and back URL to the context"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = SearchForm(auto_id=False)
        return context
