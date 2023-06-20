from datetime import datetime, timezone, timedelta
from random import randint
from django.test import TestCase

from jobseeker.models import Jobseeker
from resumes.models import Resume
from resumes.forms import ResumeSearchForm


def get_random_date():
    """Return random date from the last 100 days"""
    random_days = randint(0, 100)
    random_hours = randint(0, 24)
    random_minutes = randint(0, 60)
    return datetime.now(timezone.utc) - timedelta(
        days=random_days, hours=random_hours, minutes=random_minutes
    )


class TestEmployerHomeView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create 10 jobseeker users with profiles
        # profile and role are created automatically
        for i in range(1, 11):
            Jobseeker.objects.create_user(
                email=f"jobseeker{i}@email.com",
                password="12345678",
            )
        # Create 5 active and 5 inactive resumes
        cls.active_resumes = [
            Resume.objects.create(
                jobseeker=Jobseeker.objects.get(id=i),
                occupation=f"Active {i}",
                status=Resume.ResumePublishStatus.ACTIVE,
            )
            for i in range(1, 6)
        ]
        cls.inactive_resumes = [
            Resume.objects.create(
                jobseeker=Jobseeker.objects.get(id=i),
                occupation=f"In Review {i}",
                status=Resume.ResumePublishStatus.IN_REVIEW,
            )
            for i in range(6, 11)
        ]

        # set random created_on date for all resumes
        for vac in cls.active_resumes + cls.inactive_resumes:
            vac.created_on = get_random_date()
            vac.save()

    def test_load_employer_home_page(self):
        """Test that home page is loaded"""
        response = self.client.get("/employer")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employer/home.html")

    def test_get_4_active_resumes(self):
        """Test that only 4 active resumes are returned"""
        response = self.client.get("/employer")
        self.assertEqual(response.status_code, 200)

        resume_list = response.context["resume_list"]

        # check that only 4 resumes are returned
        self.assertEqual(len(resume_list), 4)

        # check that all 4 resumes are active
        for resume in resume_list:
            self.assertEqual(resume.status, Resume.ResumePublishStatus.ACTIVE)

    def test_get_resumes_ordered_by_created_date(self):
        """Test that resumes are ordered by created date"""
        response = self.client.get("/employer")
        self.assertEqual(response.status_code, 200)

        resume_list = response.context["resume_list"]

        for i, res in enumerate(resume_list):
            if i == 3:
                break
            self.assertGreaterEqual(
                res.created_on, resume_list[i + 1].created_on
            )

    def test_search_form_in_context(self):
        """Test that search form is in the context"""
        response = self.client.get("/employer")
        self.assertEqual(response.status_code, 200)

        context = response.context

        self.assertIn("form", context)
        self.assertIn("nav_form", context)

        self.assertIsInstance(context["form"], ResumeSearchForm)
        self.assertIsInstance(context["nav_form"], ResumeSearchForm)
