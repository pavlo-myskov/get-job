from django.test import TestCase
from django.urls import reverse

from jobseeker.models import Jobseeker
from resumes.models import Resume


class TestResumeListView(TestCase):
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

    def test_load_resume_list_template(self):
        """
        Test that resume list template is loaded
        """
        response = self.client.get(reverse("resume_search"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resumes/resume_list.html")

    def test_get_full_list_of_active_resumes(self):
        """
        Test that all active resumes are returned
        """
        response = self.client.get(reverse("resume_search"))
        resume_list = response.context["resume_list"]

        self.assertEqual(len(resume_list), 5)
        self.assertQuerysetEqual(
            resume_list, self.active_resumes, ordered=False
        )

    def test_get_resumes_by_keywords_in_occupation(self):
        """
        Test that resumes are filtered by keywords in occupation
        """
        search_query = {"keywords": "1, 3"}
        response = self.client.get(reverse("resume_search"), search_query)
        resume_list = response.context["resume_list"]

        self.assertEqual(len(resume_list), 2)
        self.assertQuerysetEqual(
            resume_list,
            [self.active_resumes[0], self.active_resumes[2]],
            ordered=False,
        )
