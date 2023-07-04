from django import forms

from resumes.models import Resume
from .models import Application, Vacancy


class SearchForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ["title", "area", "job_location", "job_type"]

    def __init__(self, *args, **kwargs):
        """Override init method to set custom settings for fields"""
        super().__init__(*args, **kwargs)

        # set fields as not required
        for field in self.fields.values():
            field.required = False

        self.fields["title"].label = "Job Title"

        # set first area choice to 'All' instead of '---------'
        area_choices = self.fields["area"].choices
        area_choices[0] = ("", "All")
        self.fields["area"].choices = area_choices

        # set first job_location choice to 'All' instead of '---------'
        job_location_choices = self.fields["job_location"].choices
        job_location_choices[0] = ("", "All")
        self.fields["job_location"].choices = job_location_choices

        # set first job_type choice to 'All' instead of '---------'
        job_type_choices = self.fields["job_type"].choices
        job_type_choices[0] = ("", "All")
        self.fields["job_type"].choices = job_type_choices

        # set custom widget attributes
        self.fields["title"].widget.attrs.update(
            {
                "class": "form-control search-bar royalpurple-input",
                "type": "search",
                "aria-label": "Search job",
                "placeholder": "search keywords",
            }
        )
        self.fields["area"].widget.attrs.update(
            {
                "class": "royalpurple-input form-select",
                "aria-label": "Select area",
            }
        )
        self.fields["job_location"].widget.attrs.update(
            {
                "class": "royalpurple-input form-select",
                "aria-label": "Select job location",
            }
        )
        self.fields["job_type"].widget.attrs.update(
            {
                "class": "royalpurple-input form-select",
                "aria-label": "Select job type",
            }
        )


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["resume", "cover_letter"]

        labels = {
            "resume": "Select your resume",
        }
        widgets = {
            "resume": forms.RadioSelect,
            "cover_letter": forms.Textarea(
                attrs={
                    "class": "form-control royalpurple-input",
                    "aria-label": "Cover letter",
                    "placeholder": "Introduce yourself to the employer",
                    "maxlength": 1000,
                }
            ),
        }
        error_messages = {
            "cover_letter": {
                "max_length": "Cover letter must be less than 1000 characters",
            }
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        # set resume choices to resumes that are active of the logged in user
        self.fields["resume"].queryset = self.request.user.resumes.filter(
            status=Resume.ResumePublishStatus.ACTIVE
        )
