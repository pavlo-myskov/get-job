from django.utils import timezone
from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.urls import reverse

from jobseeker.models import Jobseeker, JobseekerProfile
from resumes.models import Resume


class TestResumeListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create 10 jobseeker users with profiles
        # profile and role are created automatically
        for i in range(1, 13):
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

    def test_filter_resumes_by_keywords_in_occupation(self):
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

    def test_filter_resumes_by_keywords_in_occupation_and_skills(self):
        """
        Test that resumes are filtered by keywords in skills and occupation
        """
        resume = Resume.objects.create(
            jobseeker=Jobseeker.objects.get(id=1),
            occupation="Test",
            skills="3",
            status=Resume.ResumePublishStatus.ACTIVE,
        )
        self.active_resumes.append(resume)
        search_query = {"keywords": "3"}
        response = self.client.get(reverse("resume_search"), search_query)
        resume_list = response.context["resume_list"]

        self.assertEqual(len(resume_list), 2)
        self.assertQuerysetEqual(
            resume_list,
            [
                self.active_resumes[2],
                self.active_resumes[-1],
            ],
            ordered=False,
        )

    def test_filter_resume_by_gender(self):
        """
        Test that resumes are filtered by gender
        """
        # Male resume ids - 1, 3, 5; Female - 2, 4
        for resume in self.active_resumes:
            # if even number, set gender to Female
            if resume.pk % 2 == 0:
                resume.jobseeker.profile.gender = (
                    JobseekerProfile.GENDER_TYPES[0][0]
                )
                resume.jobseeker.profile.save()
            else:
                # if odd number, set gender to Male
                resume.jobseeker.profile.gender = (
                    JobseekerProfile.GENDER_TYPES[1][0]
                )
                resume.jobseeker.profile.save()

        # search query for gender Male
        search_query = {"gender": JobseekerProfile.GENDER_TYPES[1][0]}
        response = self.client.get(reverse("resume_search"), search_query)
        resume_list = response.context["resume_list"]

        self.assertEqual(len(resume_list), 3)
        self.assertQuerysetEqual(
            resume_list,
            [
                self.active_resumes[0],
                self.active_resumes[2],
                self.active_resumes[4],
            ],
            ordered=False,
        )

    def test_filter_resume_by_experience(self):
        """
        Test that resumes are filtered by experience
        """
        self.active_resumes[
            3
        ].experience_duration = Resume.Duration.TWO_TO_5_YEARS
        self.active_resumes[3].save()

        search_query = {"experience": Resume.Duration.TWO_TO_5_YEARS}
        response = self.client.get(reverse("resume_search"), search_query)
        resume_list = response.context["resume_list"]

        self.assertEqual(len(resume_list), 1)
        self.assertEqual(resume_list[0], self.active_resumes[3])

    def test_filter_resume_by_exact_age(self):
        """
        Test that resumes are filtered by exact age 25
        """
        today = timezone.now().date()
        # set age of jobseeker as 25 years old
        self.active_resumes[1].jobseeker.profile.dob = today - relativedelta(
            years=25
        )
        self.active_resumes[1].jobseeker.profile.save()

        search_query = {"min_age": 25, "max_age": 25}
        response = self.client.get(reverse("resume_search"), search_query)
        resume_list = response.context["resume_list"]

        self.assertEqual(len(resume_list), 1)
        self.assertEqual(resume_list[0], self.active_resumes[1])

    def test_filter_resume_by_age_range_include_exlude(self):
        """
        Test that resumes are filtered by age range 18-30
        (including 18, excuding 30).

        Test ages: 17, 18, 29, 30. Correct ages: 18, 29
        """
        today = timezone.now().date()

        self.active_resumes[0].jobseeker.profile.dob = today - relativedelta(
            years=17
        )
        self.active_resumes[0].jobseeker.profile.save()

        self.active_resumes[1].jobseeker.profile.dob = today - relativedelta(
            years=18
        )
        self.active_resumes[1].jobseeker.profile.save()

        self.active_resumes[2].jobseeker.profile.dob = today - relativedelta(
            years=30
        )
        self.active_resumes[2].jobseeker.profile.save()

        self.active_resumes[3].jobseeker.profile.dob = today - relativedelta(
            years=29
        )
        self.active_resumes[3].jobseeker.profile.save()

        search_query = {"min_age": 18, "max_age": 30}
        response = self.client.get(reverse("resume_search"), search_query)
        resume_list = response.context["resume_list"]
        self.assertEqual(len(resume_list), 2)
        self.assertQuerysetEqual(
            resume_list,
            [
                self.active_resumes[1],
                self.active_resumes[3],
            ],
            ordered=False,
        )

    def test_filter_resume_by_age_max_range_more_than_65(self):
        """
        Test that resumes are filtered by age range 18 - 65+.

        Test ages: 17, 18, 65, 70. Correct result: 18, 65, 70
        """
        today = timezone.now().date()

        self.active_resumes[0].jobseeker.profile.dob = today - relativedelta(
            years=17
        )
        self.active_resumes[0].jobseeker.profile.save()

        self.active_resumes[1].jobseeker.profile.dob = today - relativedelta(
            years=18
        )
        self.active_resumes[1].jobseeker.profile.save()

        self.active_resumes[2].jobseeker.profile.dob = today - relativedelta(
            years=65
        )
        self.active_resumes[2].jobseeker.profile.save()

        self.active_resumes[3].jobseeker.profile.dob = today - relativedelta(
            years=70
        )
        self.active_resumes[3].jobseeker.profile.save()

        search_query = {"min_age": 18, "max_age": 66}
        response = self.client.get(reverse("resume_search"), search_query)
        resume_list = response.context["resume_list"]
        self.assertEqual(len(resume_list), 3)
        self.assertQuerysetEqual(
            resume_list,
            [
                self.active_resumes[1],
                self.active_resumes[2],
                self.active_resumes[3],
            ],
            ordered=False,
        )

    def test_filter_resume_by_max_age_65(self):
        """
        Test that resumes are filtered by max age 65 (excluding 65 and above).
        Test range: max_age-65. Test ages: 17, 18, 64, 65, 70.
        Correct result: 64, 65
        """
        today = timezone.now().date()

        self.active_resumes[0].jobseeker.profile.dob = today - relativedelta(
            years=17
        )
        self.active_resumes[0].jobseeker.profile.save()

        self.active_resumes[1].jobseeker.profile.dob = today - relativedelta(
            years=18
        )
        self.active_resumes[1].jobseeker.profile.save()

        self.active_resumes[2].jobseeker.profile.dob = today - relativedelta(
            years=64
        )
        self.active_resumes[2].jobseeker.profile.save()

        self.active_resumes[3].jobseeker.profile.dob = today - relativedelta(
            years=65
        )
        self.active_resumes[3].jobseeker.profile.save()

        self.active_resumes[4].jobseeker.profile.dob = today - relativedelta(
            years=70
        )
        self.active_resumes[4].jobseeker.profile.save()

        search_query = {"max_age": 65}
        response = self.client.get(reverse("resume_search"), search_query)
        resume_list = response.context["resume_list"]
        self.assertEqual(len(resume_list), 2)
        self.assertQuerysetEqual(
            resume_list,
            [
                self.active_resumes[1],
                self.active_resumes[2],
            ],
            ordered=False,
        )

    def test_filter_resume_older_than_65_1(self):
        """
        Test that resumes are filtered by only older than 65.
        Test range: only 65+. Test ages: 64, 65, 66, 70.
        Correct ages: 65, 66, 70
        """
        today = timezone.now().date()

        self.active_resumes[1].jobseeker.profile.dob = today - relativedelta(
            years=64
        )
        self.active_resumes[1].jobseeker.profile.save()

        self.active_resumes[2].jobseeker.profile.dob = today - relativedelta(
            years=65
        )
        self.active_resumes[2].jobseeker.profile.save()

        self.active_resumes[3].jobseeker.profile.dob = today - relativedelta(
            years=66
        )
        self.active_resumes[3].jobseeker.profile.save()

        self.active_resumes[4].jobseeker.profile.dob = today - relativedelta(
            years=70
        )
        self.active_resumes[4].jobseeker.profile.save()

        search_query = {"min_age": 66, "min_age": 66}
        response = self.client.get(reverse("resume_search"), search_query)
        resume_list = response.context["resume_list"]
        self.assertEqual(len(resume_list), 3)
        self.assertQuerysetEqual(
            resume_list,
            [
                self.active_resumes[2],
                self.active_resumes[3],
                self.active_resumes[4],
            ],
            ordered=False,
        )

    def test_filter_resume_older_than_65_2(self):
        """
        Test that resumes are filtered by only older than 65.
        Test range: 65 - 65+. Test ages: 64, 65, 66, 70.
        Correct ages: 65, 66, 70
        """
        today = timezone.now().date()

        self.active_resumes[1].jobseeker.profile.dob = today - relativedelta(
            years=64
        )
        self.active_resumes[1].jobseeker.profile.save()

        self.active_resumes[2].jobseeker.profile.dob = today - relativedelta(
            years=65
        )
        self.active_resumes[2].jobseeker.profile.save()

        self.active_resumes[3].jobseeker.profile.dob = today - relativedelta(
            years=66
        )
        self.active_resumes[3].jobseeker.profile.save()

        self.active_resumes[4].jobseeker.profile.dob = today - relativedelta(
            years=70
        )
        self.active_resumes[4].jobseeker.profile.save()

        search_query = {"min_age": 66, "min_age": 66}
        response = self.client.get(reverse("resume_search"), search_query)
        resume_list = response.context["resume_list"]
        self.assertEqual(len(resume_list), 3)
        self.assertQuerysetEqual(
            resume_list,
            [
                self.active_resumes[2],
                self.active_resumes[3],
                self.active_resumes[4],
            ],
            ordered=False,
        )

    def test_get_bound_form(self):
        """
        Test that bound form is returned with search queries
        """
        search_query = {
            "keywords": "test",
            "gender": JobseekerProfile.GENDER_TYPES[2][0],
            "min_age": 20,
            "max_age": 30,
        }
        response = self.client.get(reverse("resume_search"), search_query)
        response_form = response.context["form"]

        self.assertEqual(response_form["keywords"].value(), "test")
        self.assertEqual(
            response_form["gender"].value(),
            JobseekerProfile.GENDER_TYPES[2][0],
        )
        self.assertEqual(response_form["min_age"].value(), '20')
        self.assertEqual(response_form["max_age"].value(), '30')
        self.assertFalse(response_form["experience"].value())

    def test_form_errors(self):
        """
        Test that form errors are returned if form fields are invalid
        """
        search_query = {
            "keywords": "test",
            "gender": "invalid",
            "experience": "invalid",
            "min_age": "15",
            "max_age": "68",
        }
        response = self.client.get(reverse("resume_search"), search_query)
        response_form = response.context["form"]

        # no errors for keywords
        self.assertFalse(response_form["keywords"].errors)
        # name of fields is in errors
        self.assertIn('gender', response_form.errors)
        self.assertIn('experience', response_form.errors)
        self.assertIn('min_age', response_form.errors)
        self.assertIn('max_age', response_form.errors)

    def test_pagination(self):
        for i in range(6, 13):
            Resume.objects.create(
                jobseeker=Jobseeker.objects.get(id=i),
                occupation=f"Active {i}",
                status=Resume.ResumePublishStatus.ACTIVE,
            )

        response = self.client.get(reverse("resume_search"))
        page_obj = response.context["page_obj"]
        resume_list = response.context["resume_list"]

        self.assertEqual(len(resume_list), 6)
        self.assertEqual(page_obj.paginator.count, 12)
        self.assertEqual(page_obj.paginator.num_pages, 2)
        self.assertEqual(page_obj.number, 1)


class TestResumeDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(1, 5):
            Jobseeker.objects.create_user(
                email=f"jobseeker{i}@email.com",
                password="12345678",
            )
        # Create 5 active and 5 inactive resumes
        cls.resumes = [
            Resume.objects.create(
                jobseeker=Jobseeker.objects.get(id=i),
                occupation=f"Active {i}",
                status=Resume.ResumePublishStatus.ACTIVE,
            )
            for i in range(1, 5)
        ]
        cls.inactive_resumes = [
            Resume.objects.create(
                jobseeker=Jobseeker.objects.get(id=i),
                occupation=f"In Review {i}",
                status=Resume.ResumePublishStatus.IN_REVIEW,
            )
            for i in range(1, 2)
        ]

    def test_load_job_detail_template(self):
        """
        Test that resume detail template is loaded
        """
        response = self.client.get(reverse("resume_detail", args=(1,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resumes/resume_detail.html")

    def test_get_resume_detail(self):
        """
        Test that resume detail is returned
        """
        response = self.client.get(reverse("resume_detail", args=(4,)))
        resume = response.context["resume"]

        self.assertEqual(resume, self.resumes[3])

    def test_get_inactive_resume_detail(self):
        """
        Test that inactive resume detail is not returned
        """
        response = self.client.get(reverse("resume_detail", args=(5,)))

        self.assertEqual(response.status_code, 404)

    def test_get_resume_detail_with_invalid_id(self):
        """
        Test that invalid resume id returns 404
        """
        response = self.client.get(reverse("resume_detail", args=(10,)))

        self.assertEqual(response.status_code, 404)

    def test_get_context(self):
        """
        Test that context is returned with resume and nav_form
        """
        response = self.client.get(reverse("resume_detail", args=(1,)))
        context = response.context

        self.assertIn("resume", context)
        self.assertIn("nav_form", context)
