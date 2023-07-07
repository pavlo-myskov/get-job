import re
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.db.models import QuerySet
from jobs.forms import SearchForm

from users.models import User
from .models import Resume
from .forms import ResumeSearchForm, ResumeCreateForm
from jobseeker.views import JobseekerRequiredMixin


def get_keywords(search_data: dict) -> Q:
    """Extract keywords from search data with regex
    and return Q object with keywords"""

    # extract keywords from string using regex
    keywords_string = search_data.get("keywords", "").strip()
    keywords_list = re.findall(r"\w+", keywords_string)

    # "Search for multiple keywords over multiple columns in Django"
    # code snippet based on stackoverflow answer:
    # https://stackoverflow.com/a/43552495/20143678
    if keywords_list:
        keywords_obj = Q(occupation__icontains=keywords_list[0]) | Q(
            skills__icontains=keywords_list[0]
        )
        for keyword in keywords_list[1:]:
            keywords_obj.add(
                Q(occupation__icontains=keyword)
                | Q(skills__icontains=keyword),
                keywords_obj.connector,
            )
    else:
        keywords_obj = Q()

    return keywords_obj


def get_age_lookup(search_data: dict) -> Q:
    """Return lookup for age range from search data"""
    today = timezone.now().date()
    max_age = search_data.get("max_age", 66)
    min_age = search_data.get("min_age", 18)
    if min_age > max_age:
        min_age, max_age = max_age, min_age

    if min_age == max_age:
        # get all ages that are equal or older than 65
        if min_age == 66:
            dob_val = today - relativedelta(years=max_age - 1)
            lookup = Q(jobseeker__jobseekerprofile__dob__lte=dob_val)
        else:
            # if min_age and max_age are equal, search for exact age
            dob_val = today - relativedelta(years=min_age)
            lookup = Q(
                jobseeker__jobseekerprofile__dob__range=[
                    dob_val - relativedelta(years=1),
                    dob_val,
                ]
            )

    # if max_age is 66, search for all ages from min_age to 66 and older
    elif max_age == 66:
        startdate = today - relativedelta(years=min_age)
        lookup = Q(jobseeker__jobseekerprofile__dob__lte=startdate)

    else:
        # search for all ages from min_age to max_age(not including max_age)
        startdate = (
            today - relativedelta(years=max_age) + relativedelta(days=1)
        )
        enddate = today - relativedelta(years=min_age)
        lookup = Q(
            jobseeker__jobseekerprofile__dob__range=[startdate, enddate]
        )
    return lookup


def filter_resumes(search_data: dict) -> QuerySet:
    """
    Filter resumes by search data using Q objects
    """
    query = Q()
    # add Q objects to query if it is exist in search data
    if search_data.get("keywords"):
        query.add(get_keywords(search_data), query.connector)
    if search_data.get("experience"):
        query.add(
            Q(experience_duration__contains=search_data["experience"]),
            query.connector,
        )
    if search_data.get("gender"):
        # Lookups that span relationships
        query.add(
            Q(
                jobseeker__jobseekerprofile__gender__contains=search_data[  # noqa
                    "gender"
                ]
            ),
            query.connector,
        )
    if search_data.get("min_age") or search_data.get("max_age"):
        query.add(get_age_lookup(search_data), query.connector)
    # filter active resumes by search query
    # distinct() removes duplicate results
    resume_list = Resume.objects.active().filter(query).distinct()

    return resume_list


class ResumeListView(ListView):
    paginate_by = 6

    def get_queryset(self):
        """
        Search for aproved resumes by title if search query is provided,
        otherwise return all approved resumes (even if empty query is provided)
        """
        # get search query from search panel if it is provided,
        # otherwise prepopulate the search form with the session data
        # if session data is also not provided return all approved resumes
        if self.request.GET:
            self.form = ResumeSearchForm(self.request.GET)
        elif self.request.session.get("resume_search_query"):
            self.form = ResumeSearchForm(
                self.request.session.get("resume_search_query")
            )
        else:
            self.form = ResumeSearchForm()
            return Resume.objects.active()

        # if form is valid, search for resumes
        if self.form.is_valid():
            # filter only non-empty fields
            search_data = {
                key: value
                for key, value in self.form.cleaned_data.items()
                if value
            }
            # if search data is empty:
            # - return unboud form
            # - update session with empty search query
            # - return all approved resumes
            if not search_data:
                self.form = ResumeSearchForm()
                self.request.session["resume_search_query"] = {}
                resume_list = Resume.objects.active()
            else:
                # update session with the new search query if it is provided
                if self.request.GET:
                    self.request.session[
                        "resume_search_query"
                    ] = self.form.cleaned_data

                resume_list = filter_resumes(search_data)
        else:
            # if form is not valid, return an empty queryset
            resume_list = Resume.objects.none()
        return resume_list

    def get_context_data(self, **kwargs):
        """Add search form to the context"""
        context = super().get_context_data(**kwargs)
        context["form"] = self.form

        # add age error messages to the context if they exist
        if "min_age" in self.form.errors or "max_age" in self.form.errors:
            context["age_error"] = "Age must be between 18 and 66 years"

        # create a new instance of the form to be used in the navbar
        context["nav_form"] = ResumeSearchForm(auto_id=False)

        # elided pagination
        # https://docs.djangoproject.com/en/3.2/_modules/django/core/paginator/#Paginator.get_elided_page_range
        page_obj = context["page_obj"]
        custom_page_range = page_obj.paginator.get_elided_page_range(
            number=page_obj.number, on_each_side=1, on_ends=1
        )
        context["custom_page_range"] = custom_page_range
        return context


class ResumeDetailView(DetailView):
    def get_queryset(self):
        # TODO: add test
        """Return all active resumes and all resumes of the owner
        if the user is authenticated as a jobseeker,
        so that the jobseeker can see his own unpublished resumes as well
        """
        query = Q()
        if (
            self.request.user.is_authenticated
            and self.request.user.role == User.Role.JOBSEEKER
        ):
            query = Q(jobseeker__id=self.request.user.pk)

        queryset = Resume.objects.filter(
            query | Q(status=Resume.ResumePublishStatus.ACTIVE)
        )
        return queryset

    def get_context_data(self, **kwargs):
        """Add search form to the context for navbar search bar"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = ResumeSearchForm(auto_id=False)
        return context


class MyResumeListView(JobseekerRequiredMixin, ListView):
    model = Resume
    template_name = "resumes/my_resumes.html"

    def get_queryset(self):
        # TODO: add test
        """Return all resumes of the owner,
        ordered by status, updated_on.
        Example: IN_REVIEW on top and with the latest updated_on date"""
        return Resume.objects.filter(jobseeker=self.request.user).order_by(
            "-status",
            "-updated_on",
        )

    def get_context_data(self, **kwargs):
        """Add to the context:
        - tooltips for tooltip status icons
        - search form for navbar search bar
        """
        context = super().get_context_data(**kwargs)

        # add status tooltips to the context
        tooltips = {
            Resume.ResumePublishStatus.ACTIVE: "This resume is visible"
            " to employers",
            Resume.ResumePublishStatus.IN_REVIEW: "This resume is pending"
            " approval",
            Resume.ResumePublishStatus.REJECTED: "This resume contains"
            " inappropriate content or does not meet the requirements",
            Resume.ResumePublishStatus.CLOSED: "This resume is not visible and"
            " cannot be edited",
        }
        context["tooltips"] = tooltips
        context["nav_form"] = SearchForm(auto_id=False)
        return context


class MyResumeDetailView(JobseekerRequiredMixin, DetailView):
    model = Resume
    template_name = "resumes/my_resume_detail.html"

    def get_queryset(self):
        # TODO: add test
        """Return all resumes of the owner"""
        return Resume.objects.filter(jobseeker=self.request.user)

    def get_context_data(self, **kwargs):
        """Add search form to the context for navbar search bar"""
        context = super().get_context_data(**kwargs)
        context["nav_form"] = SearchForm(auto_id=False)
        return context


class ResumeCreateView(
    JobseekerRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Resume
    form_class = ResumeCreateForm
    template_name_suffix = "_create_form"
    success_message = (
        "Your resume has been created and is "
        "<span class='text-info'>pending approval</span>"
    )

    def test_func(self):
        """Check if the user has less or equal than 10 resumes"""
        self.jobseeker_test = super().test_func()
        self.has_less_6_resumes = self.request.user.resumes.all().count() <= 4
        return self.jobseeker_test and self.has_less_6_resumes

    def handle_no_permission(self):
        """Redirect to the resume list page and show an alert,
        if the user has more than 5 resumes;
        if the user is not a jobseeker, redirect to the specific 403 page"""
        # redirect to login page if the user is not authenticated
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        if self.jobseeker_test and not self.has_less_6_resumes:
            messages.error(
                self.request,
                "The maximum number of resumes has been reached. ",
                extra_tags="modal",
            )
            return HttpResponseRedirect(reverse_lazy("my_resumes"))

        return super().handle_no_permission()

    def get_success_url(self):
        """Redirect to the 'next' url if it exists,
        otherwise to the resume detail page"""
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        return reverse("my_resume_detail", args=(self.object.id,))

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """Save the current user as a jobseeker-owner of the resume"""
        form.instance.jobseeker = self.request.user
        return super().form_valid(form)


class ResumeUpdateView(
    JobseekerRequiredMixin, SuccessMessageMixin, UpdateView
):
    # TODO: add test
    model = Resume
    form_class = ResumeCreateForm
    template_name_suffix = "_update_form"
    success_message = (
        "Your resume has been updated and is "
        "<span class='text-info'>pending approval</span>"
    )

    def test_func(self):
        """Allow only the owner to update the resume,
        if the resume is not closed"""
        self.jobseeker_test = super().test_func()
        return (
            self.jobseeker_test
            and self.request.user == self.get_object().jobseeker
            and self.get_object().status != Resume.ResumePublishStatus.CLOSED
        )

    def get_success_url(self):
        """Redirect to the resume detail page"""
        return reverse("my_resume_detail", kwargs={"pk": self.get_object().pk})

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """Set the status of the resume to IN_REVIEW"""
        form.instance.status = Resume.ResumePublishStatus.IN_REVIEW
        return super().form_valid(form)


class ResumeCloseView(
    JobseekerRequiredMixin,
    SingleObjectMixin,
    View,
):
    # TODO: add test
    http_method_names = ["post"]  # only POST requests are allowed
    model = Resume

    def test_func(self):
        # TODO: redirection tests
        """Allow only the owner to close the resume,
        if the resume is not closed yet"""
        self.jobseeker_test = super().test_func()
        return (
            self.jobseeker_test
            and self.request.user == self.get_object().jobseeker
            and self.get_object().status != Resume.ResumePublishStatus.CLOSED
        )

    # allows save object only if the transaction is successful
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Set the status of the resume to CLOSED"""
        self.object = self.get_object()
        self.object.status = Resume.ResumePublishStatus.CLOSED
        self.object.save()
        messages.success(self.request, "Your resume has been closed")
        return HttpResponseRedirect(reverse("my_resumes"))


class ResumeOpenView(
    JobseekerRequiredMixin,
    SingleObjectMixin,
    View,
):
    # TODO: add test
    http_method_names = ["post"]  # only POST requests are allowed
    model = Resume

    def test_func(self):
        # TODO: redirection tests
        """Allow only the owner to open the resume,
        if the resume is closed"""
        self.jobseeker_test = super().test_func()
        return (
            self.jobseeker_test
            and self.request.user == self.get_object().jobseeker
            and self.get_object().status == Resume.ResumePublishStatus.CLOSED
        )

    # allows save object only if the transaction is successful
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Set the status of the resume to IN_REVIEW"""
        self.object = self.get_object()
        self.object.status = Resume.ResumePublishStatus.IN_REVIEW
        self.object.save()
        messages.success(
            self.request,
            "Your resume has been opened and is awaiting approval",
        )
        return HttpResponseRedirect(reverse("my_resumes"))


class ResumeDeleteView(JobseekerRequiredMixin, DeleteView):
    model = Resume
    template_name = "resumes/my_resumes.html"
    success_message = "Your resume has been permanently deleted"
    success_url = reverse_lazy("my_resumes")

    def test_func(self):
        """Allow only the owner to delete the resume"""
        self.jobseeker_test = super().test_func()
        return (
            self.jobseeker_test
            and self.request.user == self.get_object().jobseeker
        )

    def delete(self, request, *args, **kwargs):
        """Add success message to the delete view"""
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
