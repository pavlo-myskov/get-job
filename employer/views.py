from django.views.generic import ListView

from resumes.models import Resume
from resumes.forms import ResumeSearchForm


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
