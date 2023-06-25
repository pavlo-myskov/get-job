from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="jobseeker_home"),
    path(
        "jobseeker/profile/update",
        views.JobseekerProfileUpdateView.as_view(),
        name="jobseeker_profile_update",
    ),
]
