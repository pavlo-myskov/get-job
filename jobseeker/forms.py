from django.forms import (
    ModelForm,
    Textarea,
    DateInput,
    RegexField,
)

from .models import JobseekerProfile
from jobseeker.models import img_validator

# get the allowed image types from the validator
img_types = [
    img_type.replace("image/", "") for img_type in img_validator.content_types
]
# regex for phone number validation


class JobseekerProfileForm(ModelForm):
    # override the default phone CharField with the RegexField
    # Code snippet based on: https://stackoverflow.com/a/19131360/20143678
    phone = RegexField(
        regex=r"^\+?1?\d{9,15}$",
        error_messages={
            "invalid": "Phone number must be entered in the format: "
            "'+1234567890'. At least 9 digits and maximum 15 digits allowed."
        },
    )

    class Meta:
        model = JobseekerProfile
        fields = ["name", "gender", "dob", "address", "phone", "avatar"]
        labels = {
            "name": "Full Name",
            "dob": "Date of Birth",
            "phone": "Phone Number",
            "avatar": "Profile Picture",
        }
        widgets = {
            "address": Textarea(attrs={"rows": 3}),
            "dob": DateInput(
                attrs={"type": "date"},
            ),
        }
        help_texts = {
            "avatar": "Upload a profile picture. "
            f"Allowed image types are:  {', '.join(img_types)}",
        }
        error_messages = {
            "phone": {
                "invalid": "Please enter a valid phone number.",
            },
        }

    def __init__(self, *args, **kwargs):
        # add royalpurple-input class to all fields
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "royalpurple-input"}
            )
