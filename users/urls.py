from django.urls import path
from . import views

urlpatterns = [
    path(
        "accounts/signup/<str:role>/",
        views.CustomSignupView.as_view(),
        name="account_signup",
    ),
    path(
        "accounts/password/change/",
        views.CustomPasswordChangeView.as_view(),
        name="account_change_password",
    ),
    path(
        "accounts/delete/",
        views.AccountDeactivateView.as_view(),
        name="account_deactivate",
    ),
    path(
        "emailnotification/toggle/",
        views.EmailNotificationToggle.as_view(),
        name="email_notification_toggle",
    ),
]
