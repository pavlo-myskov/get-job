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
]
