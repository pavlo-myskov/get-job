from django.views.generic import ListView

from .models import Vacancy


class JobListView(ListView):
    context_object_name = "job_list"
    model = Vacancy

    def get_queryset(self):
        # get the query parameter from the URL
        # e.g. /jobs?search=developer, then query = developer
        query = self.request.GET.get("search").strip()
        # TODO add test empty string
        # filter titles that contain the search query
        # icontains allows lookup is case insensitive
        if query:
            job_list = Vacancy.objects.filter(title__icontains=query)
            # TODO: add search by area using Q objects
            # (Q(title__icontains=query) | Q(area__icontains=query))
        else:
            job_list = Vacancy.objects.all()
        return job_list
