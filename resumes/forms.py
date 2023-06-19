from django import forms

from .models import Resume
from jobseeker.models import JobseekerProfile


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
        widget=forms.HiddenInput(attrs={"id": "min-age"}),
        max_value=66,
        min_value=18,
    )

    max_age = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(attrs={"id": "max-age"}),
        max_value=66,
        min_value=18,
    )
