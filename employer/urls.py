from django.urls import path

from . import views

urlpatterns = [
    path("employer", views.HomeView.as_view(), name="employer_home"),
    path(
        "employer/profile",
        views.EmployerProfileDetailView.as_view(),
        name="employer_profile",
    ),
    path(
        "employer/profile/update",
        views.EmployerProfileUpdateView.as_view(),
        name="employer_profile_update",
    ),
    path(
        "employer/favorites",
        views.FavoriteResumeList.as_view(),
        name="favorite_resumes",
    ),
    path(
        "employer/offers",
        views.MyJobOfferList.as_view(),
        name="my_job_offers",
    ),
    path(
        "resume/<int:pk>/offer",
        views.JobOfferView.as_view(),
        name="job_offer",
    ),
    path(
        "offer/<int:pk>/resume",
        views.JobOfferResumeSnapshotView.as_view(),
        name="job_offer_resume_snapshot",
    ),
]
