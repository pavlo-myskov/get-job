from django.test import TestCase
from django.urls import reverse

from jobs.models import Vacancy, Areas


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
        Test that title search query is case insensitive
        and returns only active jobs
        with the search query in the title
        """
        search_query = "JoB"
        url = "{url}?{filter}={value}".format(
            url=reverse("job_search"), filter="title", value=search_query
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
        search_query = {"title": "2"}
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]

        self.assertEqual(len(job_list), 1)
        self.assertEqual(job_list[0].title, "ActiveJob 2")

    def test_no_search_query_in_title(self):
        """
        Test that if search query is not in the title of any active job,
        no jobs are returned
        """
        search_query = {"title": "InactiveJob"}
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]

        self.assertEqual(len(job_list), 0)

    def test_empty_search_query(self):
        """
        Test that if search query is empty
        returns all active(approved) jobs
        """
        search_query = {
            "title": "",
            "area": "",
            "job_location": "",
            "job_type": "",
        }
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]
        self.assertEqual(len(job_list), 6)
        self.assertQuerysetEqual(
            job_list, self.active_vacancies, ordered=False
        )

    def test_search_by_valid_area(self):
        """
        Test that search by area returns job if area is valid from IrelandAreas
        """
        valid_job = Vacancy.objects.create(
            title="Galway City Job",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.GALWAY_CITY,
        )

        search_query = {"area": Areas.GALWAY_CITY}
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]
        self.assertEqual(len(job_list), 1)
        self.assertEqual(job_list[0], valid_job)

    def test_search_by_invalid_area(self):
        """
        Test that search by invalid area returns no jobs
        """
        Vacancy.objects.create(
            title="Invalid Area Job",
            status=Vacancy.JobPostStatus.ACTIVE,
            area="galway",
        )

        search_query = {"area": "galway"}
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]
        self.assertEqual(len(job_list), 0)

    def test_search_by_irish_area_only(self):
        """
        Test that search by Area.IRELAND returns only irish jobs
        """
        Vacancy.objects.create(
            title="Irish Job",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.CORK_CITY
        )
        Vacancy.objects.create(
            title="Irish Job",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.DONEGAL
        )
        uk_job = Vacancy.objects.create(
            title="Non Irish Job",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.UK
        )

        search_query = {"area": Areas.IRELAND}
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]
        self.assertEqual(len(job_list), 2)
        self.assertNotIn(uk_job, job_list)

    def test_search_by_dublin_area(self):
        """
        Test that search by Areas.DUBLIN_CITY returns all jobs in Dublin City
        """
        Vacancy.objects.create(
            title="City Centre Job",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.DUBLIN_CITY_CENTRE
        )
        Vacancy.objects.create(
            title="North Dublin Job",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.DUBLIN_NORTH
        )
        Vacancy.objects.create(
            title="South Dublin Job",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.DUBLIN_SOUTH
        )
        Vacancy.objects.create(
            title="West Dublin Job",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.DUBLIN_WEST
        )
        Vacancy.objects.create(
            title="Dublin County Job",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.DUBLIN_COUNTY
        )

        search_query = {"area": Areas.DUBLIN_CITY}
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]
        self.assertEqual(len(job_list), 4)
        self.assertNotIn(Areas.DUBLIN_COUNTY, job_list)

    def test_search_by_area_and_title(self):
        """
        Test that search by title and area returns job if they both match
        """
        job_1 = Vacancy.objects.create(
            title="Limerick City Job 1",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.LIMERICK_CITY,
        )
        job_11 = Vacancy.objects.create(
            title="Limerick City Job 11",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.LIMERICK_CITY,
        )
        job_2 = Vacancy.objects.create(
            title="Limerick City Job 2",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.LIMERICK_CITY,
        )

        search_query = {"area": Areas.LIMERICK_CITY, "title": "1"}
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]
        self.assertEqual(len(job_list), 2)
        self.assertNotIn(job_2, job_list)
        self.assertIn(job_1, job_list)
        self.assertIn(job_11, job_list)

    def test_search_by_valid_job_location(self):
        """
        Test that search by job location returns job if job location is valid
        """
        valid_job = Vacancy.objects.create(
            title="Remote Job",
            status=Vacancy.JobPostStatus.ACTIVE,
            job_location=Vacancy.JobLocations.REMOTE,
        )

        search_query = {"job_location": Vacancy.JobLocations.REMOTE}
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]
        self.assertEqual(len(job_list), 1)
        self.assertEqual(job_list[0], valid_job)

    def test_search_by_invalid_job_location(self):
        """
        Test that search by invalid job location returns no jobs
        """
        Vacancy.objects.create(
            title="Invalid Job Location Job",
            status=Vacancy.JobPostStatus.ACTIVE,
            job_location="invalid",
        )

        search_query = {"job_location": "invalid"}
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]
        self.assertEqual(len(job_list), 0)

    def test_search_by_job_location_title_area(self):
        """
        Test that search by title, area and job location returns job
        if they all match
        """
        job_1 = Vacancy.objects.create(
            title="Remote Job 1",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.OFFALY,
            job_location=Vacancy.JobLocations.REMOTE,
        )
        job_21 = Vacancy.objects.create(
            title="Remote Job 21",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.OFFALY,
            job_location=Vacancy.JobLocations.REMOTE,
        )
        job_2 = Vacancy.objects.create(
            title="Remote Job 2",
            status=Vacancy.JobPostStatus.ACTIVE,
            area=Areas.OFFALY,
            job_location=Vacancy.JobLocations.ON_SITE,
        )

        search_query = {
            "title": "2",
            "area": Areas.OFFALY,
            "job_location": Vacancy.JobLocations.REMOTE,
        }
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]
        self.assertEqual(len(job_list), 1)
        self.assertIn(job_21, job_list)

    def test_search_by_valid_job_type(self):
        """
        Test that search by job type returns job if job type is valid
        """
        valid_job = Vacancy.objects.create(
            status=Vacancy.JobPostStatus.ACTIVE,
            job_type=Vacancy.JobTypes.FULL_TIME,
        )

        search_query = {"job_type": Vacancy.JobTypes.FULL_TIME}
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]
        self.assertEqual(len(job_list), 1)
        self.assertEqual(job_list[0], valid_job)

    def test_search_by_invalid_job_type(self):
        """
        Test that search by invalid job type returns no jobs
        """
        Vacancy.objects.create(
            status=Vacancy.JobPostStatus.ACTIVE, job_type="trainee"
        )

        search_query = {"job_type": "trainee"}
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]
        self.assertEqual(len(job_list), 0)

    def test_search_by_job_type_and_title(self):
        """
        Test that search by job title and job type returns job
        if they both match
        """
        job_1 = Vacancy.objects.create(
            title="Full Time Job 1",
            status=Vacancy.JobPostStatus.ACTIVE,
            job_location=Vacancy.JobLocations.HYBRID,
            job_type=Vacancy.JobTypes.FULL_TIME,
        )
        job_21 = Vacancy.objects.create(
            title="Full Time Job 21",
            status=Vacancy.JobPostStatus.ACTIVE,
            job_location=Vacancy.JobLocations.ON_SITE,
            job_type=Vacancy.JobTypes.FULL_TIME,
        )
        job_2 = Vacancy.objects.create(
            title="Full Time Job 2",
            status=Vacancy.JobPostStatus.ACTIVE,
            job_location=Vacancy.JobLocations.REMOTE,
            job_type=Vacancy.JobTypes.TEMPORARY,
        )

        search_query = {
            "title": "2",
            "job_type": Vacancy.JobTypes.FULL_TIME,
        }
        response = self.client.get(reverse("job_search"), search_query)
        job_list = response.context["job_list"]
        self.assertEqual(len(job_list), 1)
        self.assertIn(job_21, job_list)

    def test_get_bound_form(self):
        """
        Test that bound form is returned with search queries
        """
        search_query = {
            "title": "job test",
            "area": Areas.WEXFORD,
        }
        response = self.client.get(reverse("job_search"), search_query)
        response_form = response.context["form"]
        self.assertEqual(response_form["title"].value(), "job test")
        self.assertEqual(response_form["area"].value(), Areas.WEXFORD)
        self.assertFalse(response_form["job_type"].value())
        self.assertFalse(response_form["job_location"].value())

    def test_form_errors(self):
        """
        Test that form errors are returned if form fields are invalid
        """
        search_query = {
            "title": "job test",
            "area": "invalid city",
        }
        response = self.client.get(reverse("job_search"), search_query)
        response_form = response.context["form"]
        self.assertEqual(
            response_form["area"].errors[0],
            "Select a valid choice."
            " invalid city is not one of the available choices.",
        )
        self.assertFalse(response_form["title"].errors)
        self.assertFalse(response_form["job_type"].errors)
        self.assertFalse(response_form["job_location"].errors)
