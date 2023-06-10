from django.test import TestCase

from ..forms import SearchForm
from ..models import Areas, Vacancy


class TestSearchForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fields = "title", "area", "job_location", "job_type"

    def test_form_fields(self):
        """Test that the form has the correct fields"""
        form = SearchForm()
        fields = list(form.fields)
        self.assertEqual(fields, list(self.fields))

    def test_form_field_labels(self):
        """Test that the form has the correct field labels"""
        form = SearchForm()
        labels = [form.fields[field].label for field in self.fields]
        self.assertEqual(
            labels, ["Job Title", "Area", "Job location", "Job type"]
        )

    def test_form_fields_not_required(self):
        """Test that the form fields are not required"""
        form = SearchForm()
        required = [form.fields[field].required for field in self.fields]
        self.assertFalse(any(required))

    def test_form_field_title_max_lenght(self):
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

    def test_form_fields_area_validation(self):
        """
        Test that the validation fails if
        the area search query is not a valid choice,
        and passes if the area search query is a valid
        """
        invalid_search_query = "invalid area"
        invalid_form = SearchForm(data={"area": invalid_search_query})
        self.assertFalse(invalid_form.is_valid())

        valid_search_query = Areas.GALWAY_CITY
        valid_form = SearchForm(data={"area": valid_search_query})
        self.assertTrue(valid_form.is_valid())

    def test_form_fields_job_location_validation(self):
        """
        Test that the validation fails if
        the job location search query is not a valid choice,
        and passes if the job location search query is a valid
        """
        invalid_search_query = "invalid location"
        invalid_form = SearchForm(data={"job_location": invalid_search_query})
        self.assertFalse(invalid_form.is_valid())

        valid_search_query = Vacancy.JobLocations.REMOTE
        valid_form = SearchForm(data={"job_location": valid_search_query})
        self.assertTrue(valid_form.is_valid())

    def test_form_fields_job_type_validation(self):
        """
        Test that the validation fails if
        the job type search query is not a valid choice,
        and passes if the job type search query is a valid
        """
        invalid_search_query = "invalid type"
        invalid_form = SearchForm(data={"job_type": invalid_search_query})
        self.assertFalse(invalid_form.is_valid())

        valid_search_query = Vacancy.JobTypes.FULL_TIME
        valid_form = SearchForm(data={"job_type": valid_search_query})
        self.assertTrue(valid_form.is_valid())

    def test_form_placeholder_default(self):
        """Test that the default placeholder is 'search job'"""
        form = SearchForm()
        default_placeholder = form.fields["title"].widget.attrs["placeholder"]
        self.assertEqual(default_placeholder, "search job")
