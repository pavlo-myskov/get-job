'''
To prevent users from overwriting existing static files,
media file uploads should be placed in a different subfolder in the bucket.
We'll handle this by creating custom storage classes for each type of storage.
'''

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
