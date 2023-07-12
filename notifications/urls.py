from django.urls import path

from . import views

urlpatterns = [
    path(
        "applications/",
        views.ApplicationNotificationList.as_view(),
        name="application_notifications",
    ),
]
