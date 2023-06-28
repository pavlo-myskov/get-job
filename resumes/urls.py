from django.urls import path

from . import views

urlpatterns = [
    path("resumes/", views.ResumeListView.as_view(), name="resume_search"),
    path(
        "resume/<int:pk>",
        views.ResumeDetailView.as_view(),
        name="resume_detail",
    ),
    path(
        "jobseeker/resume/create",
        views.ResumeCreateView.as_view(),
        name="resume_create",
    ),
]
