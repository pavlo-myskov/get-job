from django import forms

from .models import Resume
from jobseeker.models import JobseekerProfile

from mimetypes import guess_extension
from jobportal.validators import CV_TYPES

# Get the human-readable file extension from the CV_TYPES tuple,
# that used in FileValidator class to validate the uploaded CV file.
allowed_cv_types = [
    guess_extension(cv_type).replace(".", "") for cv_type in CV_TYPES
]


class ResumeSearchForm(forms.Form):
    keywords = forms.CharField(
        max_length=254,
        required=False,
        label="Occupation, skills",
        widget=forms.TextInput(
            attrs={
                "class": "form-control search-bar cyan-blue-input",
                "type": "search",
                "aria-label": "search resumes",
                "placeholder": "search keywords",
            }
        ),
    )

    experience = forms.ChoiceField(
        choices=[("", "All")] + Resume.Duration.choices,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "cyan-blue-input form-select",
                "aria-label": "Experience",
            }
        ),
    )

    gender = forms.ChoiceField(
        choices=(("", "All"),) + JobseekerProfile.GENDER_TYPES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "cyan-blue-input form-select",
                "aria-label": "Gender",
            }
        ),
    )

    min_age = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(attrs={"id": "min-age", "value": 18}),
        max_value=66,
        min_value=18,
    )

    max_age = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(attrs={"id": "max-age", "value": 66}),
        max_value=66,
        min_value=18,
    )


class ResumeCreateForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            "occupation",
            "experience_duration",
            "skills",
            "education",
            "experience",
            "body",
            "cv",
        ]
        labels = {"body": "About"}
        widgets = {
            "occupation": forms.TextInput(
                attrs={"placeholder": "enter your occupation"},
            ),
            "skills": forms.Textarea(
                attrs={
                    "rows": 1,
                    "placeholder": "add your skills",
                },
            ),
            "education": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "add your education using format:"
                    " degree, institution, year",
                }
            ),
            "experience": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "add job experience using format:"
                    " job title, company, year",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "tell potential employers about yourself",
                }
            ),
        }
        help_texts = {
            "cv": "Upload your CV in one of the following formats: "
            f"{', '.join(allowed_cv_types)}<br>"
            "Maximum file size: 512 KB",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add royalpurple-input class to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "royalpurple-input"}
            )
        # add required attribute to skills field
        self.fields["skills"].required = True
