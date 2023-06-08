from django.test import TestCase

from ..forms import SearchForm


class TestSearchForm(TestCase):
    def test_form_placeholder_default(self):
        """Test that the default placeholder is 'search job'"""
        form = SearchForm()
        default_placeholder = form.fields["title"].widget.attrs["placeholder"]

        self.assertEqual(default_placeholder, "search job")

    def test_form_field_max_lenght(self):
        """Test that the max length of the search field is 255"""
        form = SearchForm()

        max_length = form.fields["title"].max_length
        self.assertEqual(max_length, 255)

    def test_form_field_max_lenght_validation(self):
        """
        Test that the validation fails if
        the title search query is longer than 255
        """
        search_query = "a" * 256
        form = SearchForm(data={"title": search_query})
        self.assertFalse(form.is_valid())

    def test_form_title_field_required(self):
        """Test that the title search field is required"""
        form = SearchForm()
        required = form.fields["title"].required

        self.assertFalse(required)
