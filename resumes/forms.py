from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Resume
from jobseeker.models import JobseekerProfile


class ResumeSearchForm(forms.Form):
    AGE_VALIDATORS = [
        MinValueValidator(18, message="Minimum age can't be less than 18"),
        MaxValueValidator(66, message="Maximum age can't exceed 66"),
    ]

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
        validators=AGE_VALIDATORS,
    )

    max_age = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(attrs={"id": "max-age"}),
        validators=AGE_VALIDATORS,
    )
