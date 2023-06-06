from django.views.generic import ListView

from .models import Vacancy


class JobListView(ListView):
    context_object_name = "job_list"
    model = Vacancy

    def get_queryset(self):
        '''
        Search for aproved jobs by title if search query is provided,
        otherwise return all approved jobs (even if empty query is provided)
        '''
        # get the query parameter from the URL
        # e.g. /jobs?search=developer, then query = developer
        query = self.request.GET.get("search")
        # icontains allows lookup is case insensitive
        if query and query.strip():
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
