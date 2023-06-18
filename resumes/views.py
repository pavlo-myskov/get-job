from django.views.generic import ListView

from .models import Resume
from .forms import ResumeSearchForm


class ResumeListView(ListView):
    paginate_by = 6
    model = Resume

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        context = super().get_context_data(**kwargs)
        context["form"] = ResumeSearchForm(auto_id=False)
        # TODO: Implement search
        # context["form"] = self.form
        # create a new instance of the form to be used in the navbar
        context["nav_form"] = ResumeSearchForm(auto_id=False)

        # elided pagination
        # https://docs.djangoproject.com/en/3.2/_modules/django/core/paginator/#Paginator.get_elided_page_range
        page_obj = context["page_obj"]
        custom_page_range = page_obj.paginator.get_elided_page_range(
            number=page_obj.number, on_each_side=1, on_ends=1
        )
        context["custom_page_range"] = custom_page_range
        return context
