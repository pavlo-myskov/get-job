from django.http import HttpResponseRedirect
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from django.contrib import messages

from .forms import CustomSignupForm


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        """
        Redirect to the profile page of the selected role
        after successful signup
        """

        # Get selected role
        role = request.POST.get("role")
        if role == CustomSignupForm.Role.JOBSEEKER:
            redirect_url = reverse("jobseeker_profile_update")
        elif role == CustomSignupForm.Role.EMPLOYER:
            redirect_url = reverse("employer_profile_update")
        else:
            return super().get_signup_redirect_url(request)
        return redirect_url

    def get_login_redirect_url(self, request):
        """
        Redirect to the homepage of the selected role
        if no next URL is provided
        """
        if request.user.role == CustomSignupForm.Role.JOBSEEKER:
            return reverse("jobseeker_home")
        elif request.user.role == CustomSignupForm.Role.EMPLOYER:
            return reverse("employer_home")
        else:
            return super().get_login_redirect_url(request)

    def respond_user_inactive(self, request, user):
        '''
        Redirect to the signup page with an error message
        if the user is inactive
        '''
        self.add_message(
            request,
            messages.ERROR,
            "account/messages/account_inactive.txt",
            {"user": user},
        )
        return HttpResponseRedirect(reverse("account_signup"))
