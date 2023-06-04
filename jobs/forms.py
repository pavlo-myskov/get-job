from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        label=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control search-bar purple-input me-2",
                "placeholder": "e.g. Software Developer",
                "type": "search",
                "aria-label": "Search job",
            }
        ),
    )
