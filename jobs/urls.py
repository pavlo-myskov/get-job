from django.urls import path

from . import views

urlpatterns = [
    path("jobs/", views.JobListView.as_view(), name="job_search"),
    path("jobs/<int:pk>", views.JobDetailView.as_view(), name="job_detail"),
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
