from django.urls import path

from . import views

urlpatterns = [
    path('employer', views.HomeView.as_view(), name='employer_home'),
    ]
