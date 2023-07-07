from django.urls import path

from . import views

urlpatterns = [
    path("jobs/", views.JobListView.as_view(), name="job_search"),
    path("jobs/<int:pk>", views.JobDetailView.as_view(), name="job_detail"),
    path(
        "employer/jobs",
        views.MyJobListView.as_view(),
        name="my_jobs",
    ),
    path(
        "employer/job/<int:pk>",
        views.MyVacancyDetailView.as_view(),
        name="my_job_detail",
    ),
    path(
        "employer/job/create",
        views.JobCreateView.as_view(),
        name="job_create",
    ),
    path(
        "employer/job/<int:pk>/update",
        views.JobUpdateView.as_view(),
        name="job_update",
    ),
    path(
        "employer/job/<int:pk>/close",
        views.JobCloseView.as_view(),
        name="job_close",
    ),
    path(
        "employer/job/<int:pk>/open",
        views.JobOpenView.as_view(),
        name="job_open",
    ),
    path(
        "employer/job/<int:pk>/delete",
        views.JobDeleteView.as_view(),
        name="job_delete",
    ),
    path(
        "job/<int:pk>/save",
        views.JobSaveToggle.as_view(),
        name="job_save_toggle",
    ),
    path(
        "job/<int:pk>/apply",
        views.JobApplyView.as_view(),
        name="job_apply",
    ),
]
