from django.urls import path

from . import views

urlpatterns = [
    path(
        "jobseeker/resume/create",
        views.ResumeCreateView.as_view(),
        name="resume_create",
    ),
    path(
        "jobseeker/resume/<int:pk>/update",
        views.ResumeUpdateView.as_view(),
        name="resume_update",
    ),
    path(
        "jobseeker/resume/<int:pk>/close",
        views.ResumeCloseView.as_view(),
        name="resume_close",
    ),
    path(
        "jobseeker/resumes",
        views.MyResumeListView.as_view(),
        name="my_resumes",
    ),
    path(
        "resume/<int:pk>",
        views.ResumeDetailView.as_view(),
        name="resume_detail",
    ),
    path("resumes/", views.ResumeListView.as_view(), name="resume_search"),
]
