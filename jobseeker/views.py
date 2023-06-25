from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView

from jobs.models import Vacancy
from jobs.forms import SearchForm

from .models import JobseekerProfile


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


class JobseekerProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = JobseekerProfile
    fields = ["name", "gender", "dob", "address", "phone", "avatar"]

    def get_object(self, *args, **kwargs):
        """Return the jobseeker profile for the current user"""
        return self.request.user.jobseekerprofile
