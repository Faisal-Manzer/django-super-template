# pylint: disable=W0614
"""
Override base settings for staging (production with debug on)
    DEBUG: true
    PRODUCTION: true
"""


# pylint: disable=W0401
from .development import *

ALLOWED_HOSTS = SECRET['DJANGO']['ALLOWED_HOST']

MIDDLEWARE = ['django_hosts.middleware.HostsRequestMiddleware'] + \
             MIDDLEWARE + \
             ['django_hosts.middleware.HostsResponseMiddleware']

INSTALLED_APPS += [
    'storages',
    'django_hosts'
]

ROOT_HOSTCONF = '__config__.hosts'
DEFAULT_HOST = 'default'

S3 = SECRET['AWS']['S3']

AWS_ACCESS_KEY_ID = SECRET['AWS']['USER']['ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = SECRET['AWS']['USER']['SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = S3['BUCKET_NAME']

AWS_QUERYSTRING_AUTH = True
STATICFILES_STORAGE = '__config__.s3conf.StaticStorage'
DEFAULT_FILE_STORAGE = '__config__.s3conf.MediaStorage'
AWS_S3_SIGNATURE_VERSION = 's3v4'

AWS_S3_REGION_NAME = S3['REGION']
AWS_S3_CUSTOM_DOMAIN = SECRET['AWS']['CDN']['PRIMARY']
AWS_DEFAULT_ACL = None

STATIC_URL = f'http://{AWS_S3_CUSTOM_DOMAIN}/{S3["STATIC_FOLDER"]}'
MEDIA_URL = f'http://{AWS_S3_CUSTOM_DOMAIN}/{S3["MEDIA_FOLDER"]}'

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
