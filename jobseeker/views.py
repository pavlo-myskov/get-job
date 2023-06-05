from django.views.generic import ListView

from jobs.models import Vacancy
from jobs.forms import SearchForm


class HomeView(ListView):
    # object name that will be used in the template
    context_object_name = "job_list"
    # get only first 4 active vacancies
    queryset = Vacancy.objects.filter(status=Vacancy.JobPostStatus.ACTIVE)[:4]
    template_name = "jobseeker/home.html"

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        # the method allows to avoid overriding get() method
        # and adding the form to the context there
        context = super(HomeView, self).get_context_data(**kwargs)
        context["main_form"] = SearchForm(
            placeholder="e.g. full stack software developer"
        )
        context["navbar_form"] = SearchForm(placeholder="search job")
        return context
