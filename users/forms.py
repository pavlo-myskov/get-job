from django.db import models
from django import forms
from django.db import transaction
from allauth.account.forms import SignupForm, LoginForm

from jobseeker.models import JobseekerProfile
from employer.models import EmployerProfile


class CustomSignupForm(SignupForm):
    class Role(models.TextChoices):
        JOBSEEKER = ("JOBSEEKER", "Jobseeker")
        EMPLOYER = ("EMPLOYER", "Employer")

    role = forms.ChoiceField(
        choices=Role.choices,
        widget=forms.RadioSelect,
        label="Select your role",
        error_messages={"required": "Please select your role."},
        required=True,
    )
    name = forms.CharField(
        label="Full Name",
        max_length=70,
        error_messages={"required": "Please enter your full name."},
        required=True,
    )

    field_order = ["role", "email", "name", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set the initial value of role field to the value from URL parameters
        # e.g. `/accounts/signup/employer/` will set the initial value of role
        # to "employer"
        if self.initial.get("role"):
            self.fields["role"].initial = self.initial["role"]
        self.fields["name"].widget.attrs["placeholder"] = "Your name"

    @transaction.atomic  # rollback the database if there is an error
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        # override the default role field with the selected role
        user.role = self.cleaned_data["role"]
        user.save()

        # create a profile for the user based on the selected role
        match user.role:
            case self.Role.JOBSEEKER:
                JobseekerProfile.objects.create(
                    user=user, name=self.cleaned_data["name"]
                )
            case self.Role.EMPLOYER:
                pass
                EmployerProfile.objects.create(
                    user=user, name=self.cleaned_data["name"]
                )
            case _:
                raise forms.ValidationError("Invalid role")

        return user


class CustomLoginForm(LoginForm):
    remember = forms.BooleanField(
        label="Remember Me",
        required=False,
        initial=True,
    )


class PasswordConfirmationForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Please enter your password",
        error_messages={
            "required": "Please enter your password.",
        },
        required=True,
    )

    def __init__(self, user, *args, **kwargs):
        """
        Store the user model in the form instance
        """
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        """
        Check if the password is correct using the built-in
        `check_password` method of the user model.
        """
        password = self.cleaned_data.get("password")
        # The `check_password` hash the input password and compare it with the
        # user's model password that stored in the database.
        if not self.user.check_password(password):
            raise forms.ValidationError("Incorrect password.")
        return password
