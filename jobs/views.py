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
        self.form = SearchForm(self.request.GET)

        search_fields = ('title', 'area', 'job_location', 'job_type')

        if self.form.is_valid():
            # get search fields from form if they are not empty
            search_data = {
                field: self.form.cleaned_data[field]
                for field in search_fields
                if self.form.cleaned_data.get(field)
            }

            # change title to title__icontains
            if 'title' in search_data:
                search_data['title__icontains'] = search_data.pop('title')

            # search for vacancies with the provided search data
            job_list = Vacancy.objects.filter(
                **search_data,
                status=Vacancy.JobPostStatus.ACTIVE,
            )
        else:
            # if form is not valid, return an empty queryset
            job_list = Vacancy.objects.none()

        return job_list

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        # create a new instance of the form to be used in the navbar
        context["nav_form"] = SearchForm(auto_id=False)
        return context
