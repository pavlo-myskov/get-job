from django.urls import path
from . import views

urlpatterns = [
    path('accounts/signup/<str:role>/', views.CustomSignupView.as_view(),
         name='account_signup'),
]
