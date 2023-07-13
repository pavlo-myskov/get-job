from django.urls import path

from . import views

urlpatterns = [
    path(
        "applications/",
        views.ApplicationNotificationList.as_view(),
        name="application_notifications",
    ),
    path(
        "application/<int:pk>/read/",
        views.ApplicationNotificationToggleRead.as_view(),
        name="application_notification_toggle_read",
    ),
    path(
        "applications/readall/",
        views.ApplicationNotificationReadAll.as_view(),
        name="application_notifications_read_all",
    ),
    path(
        "job_offers/",
        views.JobOfferNotificationList.as_view(),
        name="job_offer_notifications",
    ),
    path(
        "job_offer/<int:pk>/read/",
        views.JobOfferNotificationToggleRead.as_view(),
        name="job_offer_notification_toggle_read",
    ),
    path(
        "job_offers/readall/",
        views.JobOfferNotificationReadAll.as_view(),
        name="job_offer_notifications_read_all",
    ),
]
