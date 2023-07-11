from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic.detail import BaseDetailView
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string

from employer.models import User
from jobs.forms import JobSearchForm
from resumes.forms import ResumeSearchForm


class RelatedUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Base Related User Mixin for views that
      require Employer or Jobseeker user"""

    def test_func(self):
        """Check if the user is a Jobseeker or an Employer"""
        return (
            self.request.user.role == User.Role.JOBSEEKER
            or self.request.user.role == User.Role.EMPLOYER
        )

    def handle_no_permission(self):
        """
        If the request is AJAX, return a JSON response with
        the HTML of the 403 page.

        Redirect to the specific page based on the user's authentication
        status and role:
        - Redirect to the login page if the user is not authenticated.
        - Display the 403 jobseeker page if the role is not JOBSEEKER.
        - Otherwise, display the default 403 page.
        """
        if self.request.is_ajax():
            error_403_html = render_to_string("errors/403.html")
            return JsonResponse(
                {"error": "Forbidden", "html_page": error_403_html},
                status=403,
            )

        if not self.request.user.is_authenticated:
            message = "Sign in or create an account to access this page"
            messages.add_message(self.request, messages.WARNING, message)
            return super().handle_no_permission()
        else:
            return super().handle_no_permission()


class ResumeSnapshotView(BaseDetailView):
    """Render the resume page from the json snapshot that is stored in
        the application instance"""
    def get(self, request, *args, **kwargs):
        resume_snapshot = self.get_object().resume_snapshot
        # deserealize the resume snapshot
        resume_deserealized = serializers.deserialize("json", resume_snapshot)
        # get the resume instance from the iterator
        resume_instance = next(resume_deserealized).object
        resume_instance.updated_on = None

        resume_html = render_to_string(
            "resumes/resume_detail_card_body.html",
            {"resume": resume_instance, "user": request.user},
        )
        return JsonResponse({"html_card": resume_html})


class VacancySnapshotView(BaseDetailView):
    """Render the vacancy page from the json snapshot that is stored in
        the job offer instance"""
    def get(self, request, *args, **kwargs):
        vacancy_snapshot = self.get_object().vacancy_snapshot
        # deserealize the vacancy snapshot
        vacancy_deserealized = serializers.deserialize(
            "json", vacancy_snapshot
        )
        # get the vacancy instance from the iterator
        vacancy_instance = next(vacancy_deserealized).object
        vacancy_instance.updated_on = None

        vacancy_html = render_to_string(
            "jobs/vacancy_detail_card_body.html",
            {"vacancy": vacancy_instance, "user": request.user},
        )
        return JsonResponse({"html_card": vacancy_html})


class JobSearchFormMixin(View):
    """Mixin to add job search form to the context"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # create a new instance of the form to be used in the navbar
        context["nav_form"] = JobSearchForm(auto_id=False)
        return context


class ResumeSearchFormMixin(View):
    """Mixin to add resume search form to the context"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # create a new instance of the form to be used in the navbar
        context["nav_form"] = ResumeSearchForm(auto_id=False)
        return context
