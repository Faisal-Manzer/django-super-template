"""Configures S3 bucket files for the server"""

from storages.backends.s3boto3 import S3Boto3Storage
from __config__.secrets import SECRET


# pylint: disable=W0223
class StaticStorage(S3Boto3Storage):
    """Set static file directory"""

    location = SECRET['AWS']['S3']['STATIC_FOLDER']


# pylint: disable=W0223
class MediaStorage(S3Boto3Storage):
    """Set media file directory"""

    location = SECRET['AWS']['S3']['MEDIA_FOLDER']
