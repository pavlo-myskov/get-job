from django.http import Http404
from allauth.account.views import SignupView

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
