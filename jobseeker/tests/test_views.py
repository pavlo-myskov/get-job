from datetime import datetime, timezone, timedelta
from random import randint
from django.test import TestCase
from employer.models import Employer

from jobs.models import Vacancy
from jobs.forms import JobSearchForm


def get_random_date():
    """Return random date from the last 100 days"""
    random_days = randint(0, 100)
    random_hours = randint(0, 24)
    random_minutes = randint(0, 60)
    return datetime.now(timezone.utc) - timedelta(
        days=random_days, hours=random_hours, minutes=random_minutes
    )


class TestJobseekerHomeView(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Create 5 active and 5 inactive vacancies"""
        cls.employer = Employer.employer.create(
            email="test_employer@email.com",
            password='123456',
        )
        cls.active_vacancies = [
            Vacancy.objects.create(
                title=f"Active {i}",
                employer=cls.employer,
                status=Vacancy.JobPostStatus.ACTIVE,
            )
            for i in range(5)
        ]
        cls.inactive_vacancies = [
            Vacancy.objects.create(
                title=f"In Review {i}",
                employer=cls.employer,
                status=Vacancy.JobPostStatus.IN_REVIEW,
            )
            for i in range(5)
        ]

        # set random created_on date for all vacancies
        for vac in cls.active_vacancies + cls.inactive_vacancies:
            vac.created_on = get_random_date()
            vac.save()

    def test_load_home_page(self):
        """Test that home page is loaded"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "jobseeker/home.html")

    def test_get_4_active_vacancies(self):
        """Test that only 4 active vacancies are returned"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        job_list = response.context["job_list"]

        # check that only 4 vacancies are returned
        self.assertEqual(len(job_list), 4)

        # check that all 4 vacancies are active
        for vac in job_list:
            self.assertEqual(vac.status, Vacancy.JobPostStatus.ACTIVE)

    def test_get_vacancies_ordered_by_created_date(self):
        """Test that vacancies are ordered by created date"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        job_list = response.context["job_list"]

        for i, vac in enumerate(job_list):
            if i == 3:
                break
            self.assertGreaterEqual(vac.created_on, job_list[i + 1].created_on)

    def test_search_form_in_context(self):
        """Test that search form is in the context"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertIn("form", context)
        self.assertIn("nav_form", context)

        self.assertIsInstance(context["form"], JobSearchForm)
        self.assertIsInstance(context["nav_form"], JobSearchForm)
