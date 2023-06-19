import re
from django.views.generic import ListView
from django.db.models import Q

from .models import Resume
from .forms import ResumeSearchForm


class ResumeListView(ListView):
    paginate_by = 6
    model = Resume

    def get_queryset(self):
        """
        Search for aproved jobs by title if search query is provided,
        otherwise return all approved jobs (even if empty query is provided)
        """
        # TODO:
        # get search query from search panel if it is provided,
        # otherwise prepopulate the search form with the session data
        # if session data is also not provided return all approved jobs
        # if self.request.GET:
        #     self.form = ResumeSearchForm(self.request.GET)
        # elif self.request.session.get("search_query"):
        #     self.form = ResumeSearchForm(
        #         self.request.session.get("search_query")
        #     )
        # else:
        #     self.form = ResumeSearchForm()
        #     return Resume.objects.filter(
        #         status=Resume.ResumePublishStatus.ACTIVE
        #     )

        self.form = ResumeSearchForm(self.request.GET)

        # if form is valid, search for vacancies
        if self.form.is_valid():

            # update session with the search query
            if self.request.GET:
                self.request.session["search_query"] = self.form.cleaned_data

            # filter only non-empty fields
            search_data = dict(
                filter(
                    lambda item: item[1],
                    self.form.cleaned_data.items(),
                )
            )
            # extract keywords from string using regex
            keywords_string = search_data.get("keywords", "").strip()
            keywords = re.findall(r"\w+", keywords_string)

            # "Search for multiple keywords over multiple columns in Django"
            # code snippet based on stackoverflow answer:
            # https://stackoverflow.com/a/43552495/20143678
            if keywords:
                keywords_obj = Q(occupation__icontains=keywords[0]) | Q(
                    skills__icontains=keywords[0]
                )
                for keyword in keywords[1:]:
                    keywords_obj.add(
                        Q(occupation__icontains=keyword)
                        | Q(skills__icontains=keyword),
                        keywords_obj.connector,
                    )
            else:
                keywords_obj = Q()

            # print(search_data.get("experience", None))

            resume_list = Resume.objects.filter(
                keywords_obj,
                experience_duration__contains=search_data.get(
                    "experience", ""
                ),
                # Lookups that span relationships
                jobseeker__jobseekerprofile__gender__contains=search_data.get(
                    "gender", ""
                ),
                status=Resume.ResumePublishStatus.ACTIVE,
            )
        else:
            # if form is not valid, return an empty queryset
            resume_list = Resume.objects.none()

        return resume_list

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        context = super().get_context_data(**kwargs)
        context["form"] = self.form

        # add age error messages to the context if they exist
        if 'min_age' in self.form.errors or 'max_age' in self.form.errors:
            context["age_error"] = "Age must be between 18 and 66 years"

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
