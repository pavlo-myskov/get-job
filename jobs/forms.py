from django import forms


class SearchForm(forms.Form):
    title = forms.CharField(
        label="Job Title",
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control search-bar purple-input",
                "type": "search",
                "aria-label": "Search job",
                "placeholder": "search job",
            }
        ),
    )
