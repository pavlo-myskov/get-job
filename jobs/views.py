from django.views.generic import ListView

from .models import Vacancy
from .forms import SearchForm


class JobListView(ListView):
    context_object_name = "job_list"
    model = Vacancy

    def get_queryset(self):
        """
        Search for aproved jobs by title if search query is provided,
        otherwise return all approved jobs (even if empty query is provided)
        """
        form = SearchForm(self.request.GET)

        if form.is_valid():
            query = form.cleaned_data["title"]
            job_list = Vacancy.objects.filter(
                title__icontains=query,
                status=Vacancy.JobPostStatus.ACTIVE,
            )
            # TODO: add search by area using Q objects
            # (Q(title__icontains=query) | Q(area__icontains=query))
        else:
            job_list = Vacancy.objects.filter(
                status=Vacancy.JobPostStatus.ACTIVE,
            )

        return job_list

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        kwargs["navbar_form"] = SearchForm(placeholder="search job")
        return super().get_context_data(**kwargs)
