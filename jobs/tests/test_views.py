from django.test import TestCase
from django.urls import reverse

from jobs.models import Vacancy


class TestJobListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.active_vacancies = [
            Vacancy.objects.create(
                title=f"ActiveJob {i}",
                status=Vacancy.JobPostStatus.ACTIVE,
            )
            for i in range(6)
        ]
        cls.inactive_vacancies = [
            Vacancy.objects.create(
                title=f"InactiveJob {i}",
                status=Vacancy.JobPostStatus.IN_REVIEW,
            )
            for i in range(4)
        ]

    def test_load_vacancy_list_template(self):
        """
        Test that vacancy list template is loaded
        """
        response = self.client.get(reverse("job_search"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "jobs/vacancy_list.html")

    def test_get_full_list_of_active_vacancies(self):
        """
        Test that all active vacancies are returned
        """
        response = self.client.get(reverse("job_search"))
        job_list = response.context["job_list"]

        self.assertEqual(len(job_list), 6)
        self.assertQuerysetEqual(
            job_list, self.active_vacancies, ordered=False
        )

    def test_case_insensitive_active_job_search(self):
        """
        Test that search query is case insensitive and returns only active jobs
        with the search query in the title
        """
        search_query = "JoB"
        url = "{url}?{filter}={value}".format(
            url=reverse("job_search"), filter="search", value=search_query
        )
        response = self.client.get(url)
        job_list = response.context["job_list"]

        self.assertEqual(len(job_list), 6)
        for vac in job_list:
            self.assertEqual(vac.status, Vacancy.JobPostStatus.ACTIVE)
            # check that search query is in the title and is case insensitive
            self.assertIn(search_query.lower(), vac.title.lower())

    def test_specific_job_title_search(self):
        """
        Test that the search query returns exactly
        one job with the specified title.
        """
        search_query = {"search": "2"}
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]

        self.assertEqual(len(job_list), 1)
        self.assertEqual(job_list[0].title, "ActiveJob 2")

    def test_no_search_query_in_title(self):
        """
        Test that if search query is not in the title of any active job,
        no jobs are returned
        """
        search_query = {"search": "InactiveJob"}
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]

        self.assertEqual(len(job_list), 0)

    def test_empty_search_query(self):
        """
        Test that if search query is empty
        returns all active(approved) jobs
        """
        search_query = " "
        url = "{url}?{filter}={value}".format(
            url=reverse("job_search"), filter="search", value=search_query
        )
        response = self.client.get(url)
        job_list = response.context["job_list"]

        self.assertEqual(len(job_list), 6)
        self.assertQuerysetEqual(
            job_list, self.active_vacancies, ordered=False
        )
