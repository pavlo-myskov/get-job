from django.urls import path

from . import views

urlpatterns = [
    path("resumes/", views.ResumeListView.as_view(), name="resume_search"),
]
