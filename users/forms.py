from django.db import models
from django import forms
from django.db import transaction
from allauth.account.forms import SignupForm, LoginForm

from jobseeker.models import JobseekerProfile
# TODO add employer profile
# from employer.models import EmployerProfile


class CustomSignupForm(SignupForm):
    class Role(models.TextChoices):
        JOBSEEKER = ("JOBSEEKER", 'Jobseeker')
        EMPLOYER = ("EMPLOYER", 'Employer')

    role = forms.ChoiceField(
        choices=Role.choices,
        widget=forms.RadioSelect,
        label='Select your role',
        error_messages={'required': 'Please select your role.'},
        required=True
    )

    field_order = ['role', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set the initial value of role field to the value from URL parameters
        # e.g. `/accounts/signup/employer/` will set the initial value of role
        # to "employer"
        if self.initial.get('role'):
            self.fields['role'].initial = self.initial['role']

    @transaction.atomic  # rollback the database if there is an error
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        # override the default role field with the selected role
        user.role = self.cleaned_data['role']
        user.save()

        # create a profile for the user based on the selected role
        match user.role:
            case self.Role.JOBSEEKER:
                JobseekerProfile.objects.create(user=user)
            case self.Role.EMPLOYER:
                pass
            # TODO: add employer profile
            #     EmployerProfile.objects.create(user=user)
            case _:
                raise forms.ValidationError("Invalid role")

        return user


class CustomLoginForm(LoginForm):
    remember = forms.BooleanField(
        label="Remember Me", required=False, initial=True,
    )
