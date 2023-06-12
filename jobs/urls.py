from django.urls import path

from . import views

urlpatterns = [
    path('jobs/', views.JobListView.as_view(), name='job_search'),
    path('jobs/<int:pk>', views.JobDetailView.as_view(), name='job_detail'),
    ]
