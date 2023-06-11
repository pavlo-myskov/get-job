from django import forms

from .models import Vacancy


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
        if hasattr(self.fields['area'], 'choices'):
            choices = self.fields['area'].choices
            if isinstance(choices, list):
                choices[0] = ('', 'All')
                self.fields['area'].choices = choices

        # set custom widget attributes
        self.fields["title"].widget.attrs.update(
            {
                "class": "form-control search-bar purple-input",
                "type": "search",
                "aria-label": "Search job",
                "placeholder": "search keywords",
            }
        )
        self.fields["area"].widget.attrs.update(
            {
                "class": "purple-input form-select",
                "aria-label": "Select area",
            }
        )
        self.fields["job_location"].widget.attrs.update(
            {
                "class": "purple-input form-select",
                "aria-label": "Select job location",
            }
        )
        self.fields["job_type"].widget.attrs.update(
            {
                "class": "purple-input form-select",
                "aria-label": "Select job type",
            }
        )
