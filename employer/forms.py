from django.forms import ModelForm, RegexField, Textarea

from jobportal.custom_cloudinary import CloudinaryFileField, allowed_img_types

from jobportal.utils import generate_filename_from_email
from jobs.models import Vacancy

from .models import EmployerProfile, JobOffer


class EmployerProfileForm(ModelForm):
    # override the default phone CharField with the RegexField
    # Code snippet based on: https://stackoverflow.com/a/19131360/20143678
    phone = RegexField(
        regex=r"^\+?1?\d{9,15}$",
        error_messages={
            "invalid": "Phone number must be entered in the format: "
            "'+1234567890' or '012345678'. At least 9 digits and"
            " maximum 15 digits allowed."
        },
        required=False,
    )

    logo = CloudinaryFileField(
        help_text="Upload a company logo. "
        f"Allowed image types are:  {', '.join(allowed_img_types)}<br>"
        "Maximum file size: 5 MB",
        label="Company Logo",
        required=False,
        options={
            "unique_filename": True,
            "overwrite": True,
            "format": "webp",
            "resource_type": "image",
            "default": "media/get-job/company_placeholder",
            "folder": "media/get-job/company_logos",
            "transformation": [
                {
                    "quality": "auto:eco",
                    "crop": "fit",
                    "width": "250",
                }
            ],
        },
    )

    class Meta:
        model = EmployerProfile
        fields = ["name", "company", "phone", "website", "logo"]
        labels = {
            "name": "Full Name",
            "company": "Company Name",
            "phone": "Phone Number",
            "website": "Company Website",
        }

    def __init__(self, *args, **kwargs):
        # add cyan-blue-input class to all fields
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "cyan-blue-input"}
            )
        # set the public_id of the logo field to the user's email
        email = self.instance.user.email
        self.fields["logo"].options[
            "public_id"
        ] = generate_filename_from_email(email)


class OfferForm(ModelForm):
    class Meta:
        model = JobOffer
        fields = ["vacancy", "message"]

        labels = {
            "vacancy": "Select a vacancy to offer",
            "message": "Message (Optional)",
        }
        widgets = {
            "message": Textarea(
                attrs={
                    "class": "form-control cyan-input",
                    "aria-label": "Message to the jobseeker",
                    "placeholder": "Write a message to the jobseeker",
                    "maxlength": 1000,
                }
            ),
        }
        error_messages = {
            "message": {
                "max_length": "Message must be less than 1000 characters",
            }
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        # get active resumes of the user and set them as list of tuples
        self.fields["vacancy"].choices = self.request.user.vacancies.filter(
            status=Vacancy.JobPostStatus.ACTIVE,
        ).values_list("id", "title")
        self.fields["vacancy"].empty_label = None
