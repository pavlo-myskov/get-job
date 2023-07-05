from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.contrib import messages

from users.models import User

from resumes.models import Resume
from resumes.forms import ResumeSearchForm


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
