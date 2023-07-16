from django.http import HttpResponseRedirect
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from django.contrib import messages

from .forms import CustomSignupForm


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        """
        Redirect to the homepage of the selected role
        if no next URL is provided.

        Note
        that URLs passed explicitly (e.g. by passing along a `next`
        GET parameter) take precedence over the value returned here.
        """
        if request.user.role == CustomSignupForm.Role.JOBSEEKER:
            return reverse("jobseeker_home")
        elif request.user.role == CustomSignupForm.Role.EMPLOYER:
            return reverse("employer_home")
        else:
            return super().get_login_redirect_url(request)

    def respond_user_inactive(self, request, user):
        """
        Redirect to the signup page with an error message
        if the user is inactive
        """
        self.add_message(
            request,
            messages.ERROR,
            "account/messages/account_inactive.txt",
            {"user": user},
        )
        return HttpResponseRedirect(reverse("account_signup"))

    def get_email_confirmation_redirect_url(self, request):
        """
        Redirect to the edit profile page of the selected role after
        successful email confirmation if the user is logged in.
        Related to ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

        After updating the profile, the user will be redirected to the
        Create Resume page if the user is a jobseeker, or the Create Job
        page if the user is an employer.
        """

        if request.user.is_authenticated:
            role = request.user.role
            if role == CustomSignupForm.Role.JOBSEEKER:
                profile_update_url = reverse("jobseeker_profile_update")
                create_resume_url = reverse("resume_create")

                # build the redirect url with the next parameter
                return profile_update_url + "?next=" + create_resume_url

            elif role == CustomSignupForm.Role.EMPLOYER:
                profile_update_url = reverse("employer_profile_update")
                create_job_url = reverse("job_create")

                return profile_update_url + "?next=" + create_job_url

        return super().get_email_confirmation_redirect_url(request)
