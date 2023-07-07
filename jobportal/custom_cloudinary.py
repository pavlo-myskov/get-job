from cloudinary.forms import CloudinaryFileField as BaseCloudinaryFileField

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


class CloudinaryFileField(BaseCloudinaryFileField):
    def to_python(self, value):
        """Override the default to_python method to add the custom validator"""
        img_validator(value)
        return super(CloudinaryFileField, self).to_python(value)
