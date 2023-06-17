from django.views.generic import ListView

from resumes.models import Resume

# from resumes.forms import SearchForm


class HomeView(ListView):
    # object name that will be used in the template
    context_object_name = "resume_list"
    # get only first 4 active resumes
    queryset = Resume.objects.filter(status=Resume.ResumePublishStatus.ACTIVE)[
        :4
    ]

    template_name = "employer/home.html"

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        context = super().get_context_data(**kwargs)

        # form = SearchForm(auto_id=False)

        # context["form"] = form
        # context["nav_form"] = SearchForm(auto_id=False)
        return context
