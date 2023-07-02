from django.views.generic import ListView, DetailView
from django.db.models import Case, When, BooleanField
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from allauth.account.utils import get_next_redirect_url

from jobs.models import Vacancy
from jobs.forms import SearchForm
from jobs.utils import annotate_saved_jobs

from users.models import User

from .models import JobseekerProfile
from .forms import JobseekerProfileForm


class JobseekerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        """Check if the user is a Jobseeker"""
        return self.request.user.role == User.Role.JOBSEEKER

    def handle_no_permission(self):
        """Display the 403 jobseeker page if the role is not JOBSEEKER."""
        return render(self.request, "errors/jobseeker_403.html", status=403)


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
        return annotate_saved_jobs(queryset, self.request)

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


class JobseekerProfileDetailView(
    LoginRequiredMixin, JobseekerRequiredMixin, DetailView
):
    model = JobseekerProfile
    template_name = "jobseeker/profile.html"
    context_object_name = "profile"

    def test_func(self):
        """Allow only the owner to view the profile"""
        jobseeker_test = super().test_func()
        return jobseeker_test and self.request.user == self.get_object().user

    def handle_no_permission(self):
        """Inherit the default handle_no_permission method
        from UserPassesTestMixin that redirects to default 403 page"""
        return super(UserPassesTestMixin, self).handle_no_permission()

    def get_object(self, queryset=None):
        """Return the jobseeker profile for the current user"""
        return self.request.user.jobseekerprofile

    def get_context_data(self, **kwargs):
        """Add search form and back URL to the context"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = SearchForm(auto_id=False)
        context["back_url"] = self._get_back_url()
        return context

    def _get_back_url(self):
        """
        Return the URL for the back button of the profile page.
        If the refferer is a child page of the profile page, return to home.
        """
        # child pages of the profile page
        child_pages = [
            reverse("jobseeker_profile_update"),
            reverse("account_change_password"),
            reverse("account_deactivate"),
        ]
        home = reverse("jobseeker_home")
        refferer = self.request.META.get("HTTP_REFERER")

        # check if the refferer exists and is a safe URL
        if refferer and url_has_allowed_host_and_scheme(
            refferer, self.request.get_host()
        ):
            # return home url if the refferer is a child page of the profile
            if any(page in refferer for page in child_pages):
                return home
            else:
                return refferer
        else:
            return home


class JobseekerProfileUpdateView(
    LoginRequiredMixin, JobseekerRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = JobseekerProfile
    form_class = JobseekerProfileForm
    template_name = "jobseeker/profile_update.html"
    success_message = "Your profile has been updated successfully"

    def test_func(self):
        """Allow only the owner to update the profile"""
        jobseeker_test = super().test_func()
        return jobseeker_test and self.request.user == self.get_object().user

    def handle_no_permission(self):
        """Inherit the default handle_no_permission method
        from UserPassesTestMixin that redirects to default 403 page"""
        return super(UserPassesTestMixin, self).handle_no_permission()

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
