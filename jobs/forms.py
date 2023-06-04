from django import forms


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # change the placeholder text depending
        # on the search bar: in navbar or in home page
        placeholder = kwargs.pop("placeholder", "search job")
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields["search"].widget.attrs["placeholder"] = placeholder

    search = forms.CharField(
        label=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control search-bar purple-input",
                "type": "search",
                "aria-label": "Search job",
            }
        ),
    )
