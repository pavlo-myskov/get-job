from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse

from allauth.account.utils import get_next_redirect_url

from jobs.models import Vacancy
from jobs.forms import SearchForm

from .models import JobseekerProfile
from .forms import JobseekerProfileForm


class HomeView(ListView):
    # object name that will be used in the template
    context_object_name = "job_list"
    # get only first 4 active vacancies
    queryset = Vacancy.objects.active()[:4]

    template_name = "jobseeker/home.html"

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
    LoginRequiredMixin, UserPassesTestMixin, DetailView
):
    model = JobseekerProfile
    template_name = "jobseeker/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        """Return the jobseeker profile for the current user"""
        return self.request.user.jobseekerprofile

    def test_func(self):
        """Allow only the owner to view the profile"""
        return self.request.user == self.get_object().user

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = SearchForm(auto_id=False)
        return context


class JobseekerProfileUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = JobseekerProfile
    form_class = JobseekerProfileForm
    template_name = "jobseeker/profile_update.html"
    success_message = "Your profile has been updated successfully"

    def get_object(self, queryset=None):
        """Return the jobseeker profile for the current user"""
        return self.request.user.jobseekerprofile

    def test_func(self):
        """Allow only the owner to update the profile"""
        return self.request.user == self.get_object().user

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
            return reverse('jobseeker_profile')


# class JobseekerProfileDeleteView(DeleteView):
#     model = JobseekerProfile
