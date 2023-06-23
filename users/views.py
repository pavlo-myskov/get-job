from django.http import Http404
from django.urls import reverse

from allauth.account.views import SignupView
from allauth.account.utils import get_next_redirect_url

from .forms import CustomSignupForm


class CustomSignupView(SignupView):
    form_class = CustomSignupForm

    def dispatch(self, request, *args, **kwargs):
        '''Check if role is valid when the user manually set the URL path
        with an invalid role,
        e.g: `/accounts/signup/invalid_role/`,
        then raise 404 error.'''
        role = self.kwargs.get('role')
        if role not in self.form_class.Role.values:
            raise Http404
        return super(SignupView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        '''Set the initial value of role field to the value from
        URL parameters.'''

        # Get initial data dict from super class
        initial = super().get_initial()

        # Get role from URL parameters
        role = self.kwargs.get('role')
        if role:
            initial['role'] = role
        return initial

    def get_success_url(self):
        '''
        Get the next URL after signup if the selected role
        is the same as the initial role.
        Otherwise, return the homepage url of the selected role
        '''

        # Get selected role
        role = self.request.POST.get('role')

        # Get initial role from URL parameters
        initial_role = self.kwargs.get('role')

        # Get next URL
        ret = (
            get_next_redirect_url(self.request, self.redirect_field_name)
            or self.success_url
        )

        # If the initial role not equal to the selected role,
        # redirect to the homepage of the selected role
        if initial_role != role:
            if role == self.form_class.Role.JOBSEEKER:
                ret = reverse('jobseeker_home')
            elif role == self.form_class.Role.EMPLOYER:
                ret = reverse('employer_home')
            else:
                raise Http404
        return ret
