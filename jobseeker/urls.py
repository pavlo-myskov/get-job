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
    # path(
    #     "jobseeker/<int:pk>/delete/",
    #     views.HomeView.as_view(),
    #     name="jobseeker_delete",
    # ),
]
