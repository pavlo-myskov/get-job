from django.test import TestCase

from ..forms import ResumeSearchForm
from ..models import Resume
from jobseeker.models import JobseekerProfile


class TestResumeSearchForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.fields = (
            "keywords",
            "experience",
            "gender",
            "min_age",
            "max_age",
        )

    def test_form_fields(self):
        """Test that the form has the correct fields"""
        form = ResumeSearchForm()
        fields = list(form.fields)
        self.assertEqual(fields, list(self.fields))

    def test_form_fields_are_not_required(self):
        """Test that the form fields are not required"""
        form = ResumeSearchForm()
        required = [form.fields[field].required for field in self.fields]
        self.assertFalse(any(required))

    def test_form_field_keywords_max_lenght(self):
        """Test that the max length of the search field is 254"""
        form = ResumeSearchForm()
        max_length = form.fields["keywords"].max_length
        self.assertEqual(max_length, 254)

    def test_form_field_experience_is_valid(self):
        """
        Test that the validation passed if
        the experience search query is a valid choice
        """
        valid_search_query = Resume.Duration.ONE_TO_2_YEARS
        valid_form = ResumeSearchForm(data={"experience": valid_search_query})
        self.assertTrue(valid_form.is_valid())

    def test_form_field_experience_is_invalid(self):
        """
        Test that the validation fails if
        the experience search query is not a valid choice
        """
        invalid_search_query = "invalid experience"
        invalid_form = ResumeSearchForm(
            data={"experience": invalid_search_query}
        )
        self.assertFalse(invalid_form.is_valid())

    def test_form_field_gender_is_valid(self):
        """
        Test that the validation passed if
        the gender search query is a valid choice
        """
        valid_search_query = JobseekerProfile.GENDER_TYPES[1][0]
        valid_form = ResumeSearchForm(data={"gender": valid_search_query})
        self.assertTrue(valid_form.is_valid())

    def test_form_field_gender_is_invalid(self):
        """
        Test that the validation fails if
        the gender search query is not a valid choice
        """
        invalid_search_query = "invalid gender"
        invalid_form = ResumeSearchForm(
            data={"gender": invalid_search_query}
        )
        self.assertFalse(invalid_form.is_valid())

    def test_form_field_min_age_is_valid(self):
        """
        Test that the validation passed if
        the min_age is in valid range (18-66) inclusive
        """

        for valid_search_query in range(18, 67):
            valid_form = ResumeSearchForm(
                data={"min_age": valid_search_query}
            )
            self.assertTrue(valid_form.is_valid())

    def test_form_field_min_age_is_invalid(self):
        """
        Test that the validation fails if
        the min_age is not in valid range
        """
        invalid_search_query = 17
        invalid_form = ResumeSearchForm(data={"min_age": invalid_search_query})
        self.assertFalse(invalid_form.is_valid())

        for invalid_search_query in [0, -1, 17, 67, 100]:
            invalid_form = ResumeSearchForm(
                data={"min_age": invalid_search_query}
            )
            self.assertFalse(invalid_form.is_valid())

    def test_form_field_max_age_is_valid(self):
        """
        Test that the validation passed if
        the max_age is in valid range (18-66) inclusive
        """

        for valid_search_query in range(18, 67):
            valid_form = ResumeSearchForm(
                data={"max_age": valid_search_query}
            )
            self.assertTrue(valid_form.is_valid())

    def test_form_field_max_age_is_invalid(self):
        """
        Test that the validation fails if
        the max_age is not in valid range
        """
        invalid_search_query = 17
        invalid_form = ResumeSearchForm(data={"max_age": invalid_search_query})
        self.assertFalse(invalid_form.is_valid())

        for invalid_search_query in [0, -1, 17, 67, 100]:
            invalid_form = ResumeSearchForm(
                data={"max_age": invalid_search_query}
            )
            self.assertFalse(invalid_form.is_valid())

    def test_form_errors(self):
        """
        Test that the form has errors when
        the fields are invalid
        """
        form1 = ResumeSearchForm(data={"experience": "invalid"})
        self.assertFalse(form1.is_valid())
        self.assertIn("experience", form1.errors)

        form2 = ResumeSearchForm(data={"gender": "invalid"})
        self.assertFalse(form2.is_valid())
        self.assertIn("gender", form2.errors)

        form3 = ResumeSearchForm(data={"min_age": 17})
        self.assertFalse(form3.is_valid())
        self.assertIn("min_age", form3.errors)

        form4 = ResumeSearchForm(data={"min_age": 67})
        self.assertFalse(form4.is_valid())
        self.assertIn("min_age", form4.errors)

        form5 = ResumeSearchForm(data={"max_age": 67})
        self.assertFalse(form5.is_valid())
        self.assertIn("max_age", form5.errors)

        form6 = ResumeSearchForm(data={"max_age": 17})
        self.assertFalse(form6.is_valid())
        self.assertIn("max_age", form6.errors)
