from django.core import serializers
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic.detail import BaseDetailView


class ResumeSnapshotView(BaseDetailView):
    def get(self, request, *args, **kwargs):
        """Render the resume page from the json snapshot that is stored in
        the application instance"""
        resume_snapshot = self.get_object().resume_snapshot
        # deserealize the resume snapshot
        resume_deserealized = serializers.deserialize("json", resume_snapshot)
        # get the resume instance from the iterator
        resume_instance = next(resume_deserealized).object
        resume_instance.updated_on = None

        resume_html = render_to_string(
            "resumes/resume_detail_card_body.html",
            {"resume": resume_instance, "user": request.user},
        )
        # TODO: add CV download
        return JsonResponse({"html_card": resume_html})


class VacancySnapshotView(BaseDetailView):
    def get(self, request, *args, **kwargs):
        """Render the vacancy page from the json snapshot that is stored in
        the job offer instance"""
        vacancy_snapshot = self.get_object().vacancy_snapshot
        # deserealize the vacancy snapshot
        vacancy_deserealized = serializers.deserialize(
            "json", vacancy_snapshot
        )
        # get the vacancy instance from the iterator
        vacancy_instance = next(vacancy_deserealized).object
        vacancy_instance.updated_on = None

        vacancy_html = render_to_string(
            "jobs/vacancy_detail_card_body.html",
            {"vacancy": vacancy_instance, "user": request.user},
        )
        return JsonResponse({"html_card": vacancy_html})
