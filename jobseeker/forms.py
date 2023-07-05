from django.forms import (
    ModelForm,
    Textarea,
    DateInput,
    RegexField,
)
from jobportal.custom_cloudinary import CloudinaryFileField, allowed_img_types
from jobportal.utils import generate_filename_from_email

from .models import JobseekerProfile


class JobseekerProfileForm(ModelForm):
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

    avatar = CloudinaryFileField(
        help_text="Upload a profile picture. "
        f"Allowed image types are:  {', '.join(allowed_img_types)}<br>"
        "Maximum file size: 5 MB",
        label="Profile Picture",
        required=False,
        options={
            "unique_filename": True,
            "overwrite": True,
            "format": "webp",
            "resource_type": "image",
            "default": "media/get-job/profile_placehoder.png",
            "folder": "media/get-job/jobseeker_avatars",
            "transformation": [
                {
                    "width": 200,
                    "height": 200,
                    "crop": "thumb",
                    "gravity": "face",
                    "quality": "auto:eco",
                    "zoom": 0.8,
                }
            ],
        },
    )

    class Meta:
        model = JobseekerProfile
        fields = ["name", "gender", "dob", "address", "phone", "avatar"]
        labels = {
            "name": "Full Name",
            "dob": "Date of Birth",
            "phone": "Phone Number",
        }
        widgets = {
            "address": Textarea(attrs={"rows": 3}),
            "dob": DateInput(
                attrs={"type": "date"},
            ),
        }

    def __init__(self, *args, **kwargs):
        # add royalpurple-input class to all fields
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "royalpurple-input"}
            )
        # set the public_id of the avatar field to the user's email
        email = self.instance.user.email
        self.fields["avatar"].options[
            "public_id"
        ] = generate_filename_from_email(email)
