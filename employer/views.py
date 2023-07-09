from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from allauth.account.utils import get_next_redirect_url
from resumes.utils import annotate_resumes

from users.models import User

from resumes.models import Resume
from resumes.forms import ResumeSearchForm

from .models import EmployerProfile
from .forms import EmployerProfileForm


class EmployerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        """Check if the user is a Employer"""
        return self.request.user.role == User.Role.EMPLOYER

    def handle_no_permission(self):
        """
        Redirect to the specific page based on the user's authentication
        status and role:
        - Redirect to the login page if the user is not authenticated.
        - Display the 403 employer page if the role is not EMPLOYER.
        - Otherwise, display the default 403 page.
        """
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
        # TODO: annotate
        # return annotate_hired_resumes(favorites, self.request)
        return favorites

    def get_context_data(self, **kwargs):
        """Add search form and back URL to the context"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = ResumeSearchForm(auto_id=False)
        return context
