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
        "jobseeker/resumes",
        views.MyResumeListView.as_view(),
        name="my_resumes",
    ),
    path(
        "jobseeker/resume/<int:pk>",
        views.MyResumeDetailView.as_view(),
        name="my_resume_detail",
    ),
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
        "jobseeker/resume/<int:pk>/open",
        views.ResumeOpenView.as_view(),
        name="resume_open",
    ),
    path(
        "jobseeker/resume/<int:pk>/delete",
        views.ResumeDeleteView.as_view(),
        name="resume_delete",
    ),
    path(
        "resume/<int:pk>/save",
        views.ResumeSaveToggle.as_view(),
        name="resume_save_toggle",
    ),
]
