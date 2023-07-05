import re
from django.forms import (
    ModelForm,
    Textarea,
    DateInput,
    RegexField,
)
from cloudinary.forms import CloudinaryFileField as BaseCloudinaryFileField

from .models import JobseekerProfile
from jobportal.validators import FileValidator


img_validator = FileValidator(
    max_size=5 * 1024 * 1024,  # 5 MB
    content_types=[
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/svg+xml",
        "image/gif",
        "image/tiff",
        "image/bmp",
        "image/jpg",
    ],
)

allowed_img_types = [
    img_type.replace("image/", "") for img_type in img_validator.content_types
]


def generate_filename_from_email(email: str):
    """
    Generate a filename from the user's email.
    Replace all non-alphanumeric characters to underscores.
    """
    pattern = r"[^a-zA-Z0-9]"
    return re.sub(pattern, "_", email)


class CloudinaryFileField(BaseCloudinaryFileField):
    def to_python(self, value):
        """Override the default to_python method to add the custom validator"""
        img_validator(value)
        return super(CloudinaryFileField, self).to_python(value)


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
