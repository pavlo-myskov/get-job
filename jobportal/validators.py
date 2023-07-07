import magic
from mimetypes import guess_extension, guess_type

from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError


# Microsoft Office MIME types for HTTP content streaming:
# https://stackoverflow.com/a/4212908/20143678
# pdf, doc, txt, docx
CV_TYPES = (
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
)


# Code snippet from stackoverflow.com answer:
# https://stackoverflow.com/a/27916582/20143678
@deconstructible
class FileValidator(object):
    error_messages = {
        "max_size": (
            "Ensure this file size is not greater than %(max_size)s."
            " Your file size is %(size)s."
        ),
        "min_size": (
            "Ensure this file size is not less than %(min_size)s. "
            "Your file size is %(size)s."
        ),
        "content_type": "Files of type %(content_type)s are not supported.",
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if not data:
            return
        if self.max_size is not None and data.size > self.max_size:
            params = {
                "max_size": filesizeformat(self.max_size),
                "size": filesizeformat(data.size),
            }
            raise ValidationError(
                self.error_messages["max_size"], "max_size", params
            )

        if self.min_size is not None and data.size < self.min_size:
            params = {
                "min_size": filesizeformat(self.min_size),
                "size": filesizeformat(data.size),
            }
            raise ValidationError(
                self.error_messages["min_size"], "min_size", params
            )

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                # convert mime type to human readable format
                try:
                    res = guess_extension(content_type) or guess_type(content_type)[0]  # noqa
                    readable_content_type = res or content_type
                except Exception:
                    readable_content_type = content_type
                params = {"content_type": readable_content_type}
                raise ValidationError(
                    self.error_messages["content_type"], "content_type", params
                )

    def __eq__(self, other):
        return (
            isinstance(other, FileValidator)
            and self.max_size == other.max_size
            and self.min_size == other.min_size
            and self.content_types == other.content_types
        )
