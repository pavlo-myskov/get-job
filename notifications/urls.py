from django.urls import path

from . import views

urlpatterns = [
    path(
        "applications/",
        views.ApplicationNotificationList.as_view(),
        name="application_notifications",
    ),
    path(
        "applications/<int:pk>/read/",
        views.ApplicationNotificationToggleRead.as_view(),
        name="application_notification_toggle_read",
    ),
    path(
        "applications/readall/",
        views.ApplicationNotificationReadAll.as_view(),
        name="application_notifications_read_all",
    ),
]
