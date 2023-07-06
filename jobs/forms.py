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

        # get active resumes of the user and set them as list of tuples
        self.fields["resume"].choices = self.request.user.resumes.filter(
            status=Resume.ResumePublishStatus.ACTIVE
        ).values_list("id", "occupation")
        self.fields["resume"].empty_label = None


class JobCreateForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = [
            "title",
            "area",
            "job_location",
            "job_type",
            "salary",
            # "experience_duration",
            "body"
        ]
        labels = {"body": "Job Description"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add cyan-input class to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "cyan-input"}
            )
