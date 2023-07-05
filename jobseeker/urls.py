from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="jobseeker_home"),
    path(
        "jobseeker/profile",
        views.JobseekerProfileDetailView.as_view(),
        name="jobseeker_profile",
    ),
    path(
        "jobseeker/profile/update",
        views.JobseekerProfileUpdateView.as_view(),
        name="jobseeker_profile_update",
    ),
    path(
        "jobseeker/favorites",
        views.FavoriteJobList.as_view(),
        name="favorite_jobs",
    ),
    path(
        "jobseeker/applications",
        views.AppliedJobList.as_view(),
        name="applied_jobs",
    ),
]
