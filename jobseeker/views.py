from django.shortcuts import render
from django.views.generic import ListView

from jobs.models import Vacancy


class HomeView(ListView):
    # object name that will be used in the template
    context_object_name = 'job_list'
    # get only first 4 active vacancies
    queryset = Vacancy.objects.filter(status=Vacancy.JobPostStatus.ACTIVE)[:4]
    template_name = 'jobseeker/home.html'
